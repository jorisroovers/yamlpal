from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class InsertionTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_insert_after_date(self):
        result = self.cli.invoke(cli.cli, ["date", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-date"))

    def test_insert_after_int(self):
        result = self.cli.invoke(cli.cli, ["invoice", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-int"))

    def test_insert_after_float(self):
        result = self.cli.invoke(cli.cli, ["tax", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-float"))

    def test_insert_after_string(self):
        result = self.cli.invoke(cli.cli, ["title", "newkey: value\n", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-string"))