from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class CheckNegativeTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_check_missing_value(self):
        result = self.cli.invoke(cli.cli, ["check", "title", "foo",
                                           "-f", self.get_sample_path("sample1")])

        expected = "Found value 'Invoice for purchases' for yamlpath 'title' does not match expected value 'foo'.\n"
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, expected)
