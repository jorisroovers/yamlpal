import yamlpal
import click


@click.command()
@click.version_option(version=yamlpal.__version__)
def cli():
    """ Simple tool for inserting new entries in yaml files while keeping the original structure and formatting  """
    click.echo("hello world!")


if __name__ == "__main__":
    cli()
