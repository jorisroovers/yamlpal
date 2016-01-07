from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from yamlpal import __version__
from click.testing import CliRunner


class CLITests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_version(self):
        result = self.cli.invoke(cli.cli, ["--version"])
        self.assertEqual(result.output.split("\n")[0], "cli, version {0}".format(__version__))
