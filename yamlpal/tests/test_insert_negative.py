from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class InsertionTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_inaccurate_path_dictionary(self):
        result = self.cli.invoke(cli.cli,
                                 ["insert", "bill-to/address", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "ERROR: Path exists but not specific enough (bill-to/address).\n")

    def test_inaccurate_path_list(self):
        result = self.cli.invoke(cli.cli, ["insert", "product", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "ERROR: Path exists but not specific enough (product).\n")
