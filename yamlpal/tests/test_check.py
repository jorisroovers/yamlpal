from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class CheckTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_check_simple(self):
        result = self.cli.invoke(cli.cli, ["check", "title", "Invoice for purchases",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.exit_code, 0)

    def test_check_regex(self):
        result = self.cli.invoke(cli.cli, ["check", "title", "(.*) purchases",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.exit_code, 0)
