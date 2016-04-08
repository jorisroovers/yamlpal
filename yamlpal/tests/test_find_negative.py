from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class FindNegativeTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_inaccurate_path_dictionary(self):
        result = self.cli.invoke(cli.cli, ["find", "bill-to/address", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "ERROR: Path exists but not specific enough (bill-to/address).\n")

    def test_inaccurate_path_list(self):
        result = self.cli.invoke(cli.cli, ["find", "product", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "ERROR: Path exists but not specific enough (product).\n")
