import yamlpal
from yamlpal.yaml_parser import YamlParser
import sys
import click
import re
import os


@click.group()
@click.version_option(version=yamlpal.__version__)
def cli():
    """ Modify yaml files while keeping the original structure and formatting.  """


def get_files(passed_files):
    """ Determines which files are part of the list that will be manipulated by yamlpal by combining
    the files that are passed as commandline arguments with the files that are passed via the stdin.
    :param passed_files: list of files that is passed via cli flags (-f).
    :return: list of files that will be manipulated by yamlpal
    """
    all_files = []
    all_files.extend(passed_files)
    if not sys.stdin.isatty():
        input_paths = sys.stdin.read().split("\n")
        for input_path in input_paths:
            if input_path.strip() != "":
                all_files.append(os.path.abspath(input_path))
                # TODO(jroovers): check if valid file paths
    return all_files


@cli.command("insert")
@click.argument('needle')
@click.argument('newcontent')
@click.option('-f', '--file',
              type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True), multiple=True)
@click.option('-i', '--inline', help="Edit file inline instead of dumping it to std out", is_flag=True)
def insert(needle, newcontent, file, inline):
    """ Insert new content into a yaml file. """
    newcontent = newcontent.strip().replace("\\n", "\n").replace("\\t", "\t")

    files = get_files(file)
    for file in files:
        insert_in_file(needle, newcontent, file, inline)


def insert_in_file(needle, newcontent, file, inline):
    # read yaml file
    fp = open(file)
    filecontents = fp.read()
    fp.close()

    # parse yaml, find target line, inject new line
    data = YamlParser.load_yaml(filecontents)
    element = find_element(data, needle)
    updated_filecontents = insert_line(element.line, newcontent, filecontents)

    # write new content to file or stdout
    if inline:
        fp = open(file, "w")
        fp.write(updated_filecontents)
        fp.close()
    else:
        click.echo(updated_filecontents, nl=False)


def find_element(yaml_dict, search_str):
    """ Given a dictionary representing a yaml document and a yaml path string, find the specified element in the
        dictionary."""

    # First split on / to determine which yaml dict we are searching in
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

    # Try accessing the line of the path we are currently on. If we can't access it,
    # it means that the user has specified a path to a dict or list, without indicating an item within the
    # dictionary or list.
    try:
        node.line
    except AttributeError:
        click.echo("ERROR: Path exists but not specific enough (%s)." % search_str, err=True)
        exit(1)
    return node


def insert_line(line_nr, new_content, filecontents):
    lines = filecontents.split("\n")

    # determine the size of indentation of the line we searched for so that we can use the same indentation
    indentation_size = len(lines[line_nr]) - len(lines[line_nr].lstrip())
    # copy indentation so we use the same whitespace characters (tab, space, mix of tab and space)
    indentation_chars = lines[line_nr][0:indentation_size]

    new_content = indentation_chars + new_content
    lines.insert(line_nr + 1, new_content)

    newfile = "\n".join(lines)
    return newfile


if __name__ == "__main__":
    cli()
