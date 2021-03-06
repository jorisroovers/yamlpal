import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor
from yaml.events import AliasEvent


class LineStr(str):
    """ String that has associated line numbers """
    pass


class LineInt(int):
    """ Int that has associated line numbers """
    pass


class LineFloat(float):
    """ Float that has associated line numbers """
    pass


class LineList(list):
    """ List that has associated line numbers """


class LineDict(dict):
    """Dictionary that has an associated start and end line number"""

    def __getitem__(self, item):
        """ Convert normal dictionaries and list to LineDicts and LineLists"""
        res = super(LineDict, self).__getitem__(item)
        if isinstance(res, LineDict) or isinstance(res, LineList):
            return res
        elif isinstance(res, dict):
            return LineDict(res)
        elif isinstance(res, list):
            return LineList(res)
        return res


class YamlParser(object):
    """ Yaml parser that attaches line numbers to a dictionary that is parsed by pyYAML.

    This parser monkeypatches some internal PyYAML methods in order to add line numbers to the returned dictionary.

    In particular:

        1. We decorate PyYAML's compose_node(...) method to add line numbers to PyYAML's internal yaml node
           representation at the time tokens are read from the yaml file.

        2. When nodes are constructed into python objects, we retrieve the line number from the node representation
           and store these in a LineStr object. LineStr objects (see class defined above) are just strings that have
           an associated line number.


    Based on http://stackoverflow.com/questions/13319067/parsing-yaml-return-with-line-number

    In addition, we do some post processing (see _augment_data()) to extract line numbers of compound datastructures
    like lists or dictionaries.

    """

    @staticmethod
    def _augment_data(data):
        """
        Recursively iterate through a given dictionary, convert each dictionary along the way to a LineDict and
        give each LineDict or LineList the line number of its key. This way, every element has a line number associated
        with it. Along the way, set the end line number of compound elements (list of dicts) to the highest end line
        number of its descendants.
        :return: a dictionary representing a yaml document with line numbers associated to each key or value of the
        dictionary.
        """

        def assign_compound_line_nrs_from_atomic(compound_element, atomic_element):
            """
            Utility method to assign line and endline numbers to compound datastructures (i.e. dict or list), based on
            an atomic element that is part of that compound datastructure (e.g. a string part of a list).
             - If the start line number is lower than the current lowest start line number for the compound element,
               then reassign the start line number for the  compound element to the start line number of the atomic
               element.
             - If the end line number is higher than the current highest end line number for the compound element,
               then reassign the end line number for the compound element to the end line number of the atomic
               element.
            """
            if not hasattr(compound_element, 'line'):
                compound_element.line = atomic_element.line
            elif atomic_element.line < compound_element.line:
                compound_element.line = atomic_element.line

            if not hasattr(compound_element, 'line_end'):
                compound_element.line_end = atomic_element.line_end
            elif atomic_element.line_end > compound_element.line_end:
                compound_element.line_end = atomic_element.line_end

        if isinstance(data, dict):
            data = LineDict(data)
            # Go over the entire dictionary and recursively call this method
            for key in data.keys():
                if data[key]:
                    res = YamlParser._augment_data(data[key])
                    # If the result of our recursive call does not have a line attribute, then we know it is not an
                    # atomic element (i.e. string), so we should assign the element the line number of the key
                    if not hasattr(res, 'line'):
                        res.line = key.line
                        if hasattr(key, 'line_end'):
                            res.line_end = key.line_end

                    assign_compound_line_nrs_from_atomic(data, res)

                    data[key] = res

        elif isinstance(data, list):
            # Go over the entire list and recursively call this method
            for index, item in enumerate(data):
                res = YamlParser._augment_data(item)
                assign_compound_line_nrs_from_atomic(data, res)
                data[index] = res

        elif isinstance(data, str):
            # We're dealing with a string. Line end is just determined by the number of newlines in the string.
            if hasattr(data, 'style') and data.style == '>':
                # If we're parsing a comment line, don't count the newlines, just trust PyYAML on the endline
                pass
            else:
                # else: count the actual newlines to determine the line-end (PyYAML counts too much)
                data.line_end = data.line + data.count('\n')
        else:
            # All other scalar types
            data.line_end = data.line

        return data

    @staticmethod
    def load_yaml(filecontents):

        loader = yaml.Loader(filecontents)

        def compose_node(parent, index):
            """ Invoked when a new node (key, value or compound (dict, list) type) is created. """
            line = loader.line  # the line number where the previous token has ended (plus empty lines)

            # If we get an alias, just return the alias event, we then know how to handle it in construct_object.
            # This allows us to not follow aliases which is handy in many cases.
            # https://github.com/yaml/pyyaml/blob/a7daab723352e68a209479b781b2f03c47e5179a/lib/yaml/composer.py#L64
            if loader.check_event(AliasEvent):
                event = loader.get_event()
                event.line = line  # Do make sure we associate a line number with the alias
                return event

            # call the original compose_node
            node = Composer.compose_node(loader, parent, index)

            # In case we are dealing with a yaml list, the line numbers turn out to be off by 1 which we need to fix.
            # What the parser will do is first invoke this method with every item in the list and then invoke it again
            # with the entire list. At that point we can iterate over the list and substract 1 from the line numbers
            # of the items in the list.
            # For single items in a list, Composer.compose_node(...) returns a ScalarNode. node.value is then of type
            # str, int, float, etc. For the entire list, Composer.compose_node(...) will return a SequenceNode with
            # node.value being of type 'list'. So by checking for the type of node.value, we can figure out whether
            # we are currently processing an item in a list or the actual list itself.
            # The only additional required check is making sure that in case node.value is a list, the items in
            # node.value are not tuples (because if they are, we are dealing with a nested dictionary instead of a
            # normal list). We can do this by checking whether node.value[0] is an instance of tuple or not.
            if isinstance(node.value, list) and len(node.value) > 0:
                if not isinstance(node.value[0], tuple):
                    # We're processing a real yaml list -> substract 1 from the line numbers in the list
                    for list_node in node.value:
                        list_node.value['__line__'] -= 1

            if not isinstance(node.value, dict):
                # replace the value of the node with a dictionary that contains both the line number and value
                node.value = {"__line__": line, "__val__": node.value}

            return node

        def construct_object(node, deep=False):
            """ Invoked when PyYAML's internal nodes are converted to python types
            (e.g. ScalarNode -> str/int/float, SequenceNode -> list, MappingNode -> dictionary)
            """

            # In case we are dealing with an Alias, just convert it to a string (prepend the * again because PyYaml
            # strips it). Also add a line number.
            if isinstance(node, AliasEvent):
                data = LineStr("*" + node.anchor)
                data.line = node.line
                return data

            # retrieve previously stored line number and value, restore node.value to original value
            line = node.value['__line__']
            node.value = node.value['__val__']

            # call the original construct_object method
            data = Constructor.construct_object(loader, node, deep)

            # if the original construct_object method creating anything else then a list or dict (i.e. a str, int, float
            # datetime, etc), just wrap it in a LineStr object.
            if not (isinstance(data, dict) or isinstance(data, list)):
                if node.tag == "tag:yaml.org,2002:int":
                    data = LineInt(data)
                elif node.tag == "tag:yaml.org,2002:float":
                    data = LineFloat(data)
                else:
                    data = LineStr(data)

                # TODO(jroovers): node.start_mark.line and node.end_mark.line provide a lot of what we need. We can
                # definitely simplify this a lot. Stupid me for now finding this earlier. It doesn't provide exactly
                # what we need, especially when anchors are used (node.start_mark and node.end_mark then include
                # everything that is referenced as well). We should look into this (I've already spend 2 hrs on this
                # and wasn't able to fully figure it out)
                # data.line = node.start_mark.line
                # data.line_end = node.end_mark.line

                data.line = line
                data.line_end = node.end_mark.line

                # If the scalar node has a style, then keep that information around later
                if hasattr(node, 'style'):
                    data.style = node.style

            return data

        # monkey patch some methods from the PyYAML loader so that we can work our magic while the yaml
        # mapping is constructed
        loader.compose_node = compose_node
        loader.construct_object = construct_object

        # Parse yaml
        data = loader.get_single_data()

        # Augment the resulting dictionary with additional information numbers by analyzing it a second time
        return YamlParser._augment_data(LineDict(data))
