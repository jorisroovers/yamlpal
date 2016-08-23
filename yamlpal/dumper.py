import yaml
from yamlpal.yaml_parser import LineStr, LineDict, LineList

AUTODETERMINE_FORMAT = "__autodetermine_format__"


def _install_customer_representers():
    """ Installs custom yaml representers so that yaml.dump() can use print out our custom classes like
    LineStr, LineDict, LineList """

    # TODO(jroovers): we need to support different yaml types like Float, Int, etc so that we don't print
    # everything like a string (i.e. wrap atomic type in quotes)

    def linestr_representer(dumper, data):
        node = dumper.represent_str(str(data))
        # If the linestring was entered as a string starting with |, we want to print it in the | again, because
        # otherwise pyyaml will insert too many newlines
        if hasattr(data, 'style') and '|' == data.style:
            node.style = data.style
        return node

    def linedict_representer(dumper, data):
        return dumper.represent_dict(data)

    def linelist_representer(dumper, data):
        return dumper.represent_list(data)

    yaml.add_representer(LineStr, linestr_representer)
    yaml.add_representer(LineDict, linedict_representer)
    yaml.add_representer(LineList, linelist_representer)


def _determine_format(element):
    """Determine the format string based of the element that we're dumping.
    For compound types we dump just the value, for atomic types we dump both key and value """
    if isinstance(element, dict) or isinstance(element, list):
        return "%{value}"
    return "%{key}: %{value}\n"


def dump(file, filecontents, element, format=AUTODETERMINE_FORMAT):
    """ Given a yaml element and yamlpal format string, return the interpolated string.
        We currently support the following placeholders:
         - %{key}     -> key of the yaml element (index if you are accessing a list)
         - %{value}   -> value of the yaml element
         - %{literal} -> the string corresponding to the yaml element as it literally occurs in the file
         - %{linenr}  -> line number on which the yaml element is found
         - %{file}    -> name of the file in which the yaml element is found
    """
    if format == AUTODETERMINE_FORMAT:
        format = _determine_format(element)
    else:
        # support newlines and tabs
        format = format.replace("\\n", "\n").replace("\\t", "\t")

    result = format.replace("%{key}", str(element.key))
    result = result.replace("%{linenr}", str(element.line))
    result = result.replace("%{linenr.end}", str(element.line_end))
    result = result.replace("%{file}", file)

    # check whether %{value} occurs before printing the value, since it can be a more expensive operation
    if "%{value}" in format:
        if isinstance(element, dict) or isinstance(element, list):
            _install_customer_representers()
            value = yaml.dump(element, default_flow_style=False)
        else:
            value = str(element)
        result = result.replace("%{value}", value)

    # check whether %{literal} occurs before splitting the file, since it's a more expensive operation
    if "%{literal}" in format:
        lines = filecontents.split("\n", element.line_end + 1)  # don't split more than required
        lines_str = ""
        for i in range(element.line, element.line_end + 1):
            lines_str += lines[i] + "\n"
        result = result.replace("%{literal}", lines_str)

    return result
