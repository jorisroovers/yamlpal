import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor


class LineStr(str):
    """ String that has an associated line number """
    pass


class YamlParser(object):
    """ Yaml parser that attaches line numbers to a dictionary that is parsed by pyYAML.

    This parser monkeypatches some internal PyYAML methods in order to add line numbers to the return dictionary.

    In particular:

        1. We decorate PyYAML's compose_node(...) method to add line numbers to PyYAML's internal yaml node
           representation at the time tokens are read from the yaml file.

        2. When nodes are constructed into python objects, we retrieve the line number from the node representation
           and store these in a LineStr object. LineStr (see class defined above) are just strings that have
           and associated line number.


    Based on http://stackoverflow.com/questions/13319067/parsing-yaml-return-with-line-number
    """

    @staticmethod
    def load_yaml(file):

        loader = yaml.Loader(open(file).read())

        def compose_node(parent, index):
            """ Invoked when a new node (key, value or compound (dict, list) type) is created. """
            line = loader.line  # the line number where the previous token has ended (plus empty lines)

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

            # replace the value of the node with a dictionary that contains both the line number and value
            node.value = {"__line__": line, "__val__": node.value}

            return node

        def construct_object(node, deep=False):
            """ Invoked when PyYAML's internal nodes are converted to python types
            (e.g. ScalarNode -> str/int/float, SequenceNode -> list, MappingNode -> dictionary)
            """
            # retrieve previously stored line number and value, restore node.value to original value
            line = node.value['__line__']
            node.value = node.value['__val__']

            # call the original construct_object method
            data = Constructor.construct_object(loader, node, deep)

            # if the original construct_object method creating anything else then a list or dict (i.e. a str, int, float
            # datetime, etc), just wrap it in a LineStr object.
            if not (isinstance(data, dict) or isinstance(data, list)):
                data = LineStr(data)
                data.line = line
            return data

        # monkey patch some methods from the PyYAML loader so that we can work our magic while the yaml
        # mapping is constructed
        loader.compose_node = compose_node
        loader.construct_object = construct_object

        return loader.get_single_data()
