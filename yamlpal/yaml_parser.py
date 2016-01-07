import yaml
from yaml.composer import Composer
from yaml.constructor import Constructor


class LineStr(str):
    """ String that has an associated line number """
    pass


class YamlParser(object):
    """ Yaml parser that attaches line numbers to a dictionary that is parsed by pyYAML.
    Based on http://stackoverflow.com/questions/13319067/parsing-yaml-return-with-line-number
    """

    @staticmethod
    def load_yaml(file):

        loader = yaml.Loader(open(file).read())

        def compose_node(parent, index):
            # the line number where the previous token has ended (plus empty lines)
            line = loader.line
            node = Composer.compose_node(loader, parent, index)

            # TODO(jroovers): special case -> document better
            if isinstance(node.value, list) and len(node.value) > 0:
                if not isinstance(node.value[0], tuple):
                    # Processing a real yaml list -> substract 1
                    for list_node in node.value:
                        list_node.value['__line__'] -= 1

            node.value = {"__line__": line, "__val__": node.value}

            return node

        def construct_object(node, deep=False):
            line = node.value['__line__']
            node.value = node.value['__val__']
            data = Constructor.construct_object(loader, node, deep)
            if isinstance(data, str):
                data = LineStr(data)
                data.line = line
            return data

        loader.compose_node = compose_node
        loader.construct_object = construct_object

        return loader.get_single_data()
