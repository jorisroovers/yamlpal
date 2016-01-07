import yamlpal
from yamlpal.yaml_parser import YamlParser
import click
import re


@click.command()
@click.argument('needle')
@click.argument('newtext')
@click.argument('file', type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True))
@click.version_option(version=yamlpal.__version__)
def cli(needle, newtext, file):
    """ Simple tool for inserting new entries in yaml files while keeping the original structure and formatting  """
    newtext = newtext.replace("\\n", "\n").replace("\\t", "\t")
    data = YamlParser.load_yaml(file)
    element = find_element(data, needle)
    inject_line(element.line, newtext, file)


def find_element(yaml_dict, search_str):
    """ Given a dictionary representing a yaml document and a yaml path string, find the specified element in the
        dictionary."""
    dict_parts = search_str.split("/")
    parsed_parts = []

    for dict_part in dict_parts:
        matches = re.match("(.*)(\[([0-9]+)\])", dict_part)
        if matches:
            list_name = matches.groups()[0]
            list_index = int(matches.groups()[2])
            parsed_parts.append(list_name)
            parsed_parts.append(list_index)
        else:
            parsed_parts.append(dict_part)

    # traverse the yaml path
    node = yaml_dict
    try:
        for key in parsed_parts:
            node = node[key]
    except (KeyError, IndexError):
        click.echo("ERROR: Invalid search string '%s'." % search_str, err=True)
        exit(1)
    try:
        node.line
    except AttributeError:
        click.echo("ERROR: Path exists but not specific enough (%s)." % search_str, err=True)
        exit(1)
    return node


def inject_line(needle_line, new_content, file):
    file_contents = open(file).readlines()

    # determine the indentation of the line we searched for so that we can use the same indentation
    indentation_size = len(file_contents[needle_line]) - len(file_contents[needle_line].lstrip())
    indentation_chars = file_contents[needle_line][0:indentation_size]

    new_content = indentation_chars + new_content
    file_contents.insert(needle_line + 1, new_content)

    for line in file_contents:
        click.echo(line, nl=False)


if __name__ == "__main__":
    cli()
