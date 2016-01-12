from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class InsertionTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_insert_inline(self):
        with self.copy_sample("sample1") as copy_path:
            result = self.cli.invoke(cli.cli, ["insert", "--inline", "title", "newkey: value", copy_path])
            actual = open(copy_path).read()
            self.assertEqual(result.output, "")
            self.assertEqual(actual, self.get_expected("sample1-after-string"))

    def test_insert_ignore_leading_trailing_whitespace(self):
        result = self.cli.invoke(cli.cli, ["insert", "title", "   newkey: value \t \n",
                                           self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-string"))

    def test_insert_after_date(self):
        result = self.cli.invoke(cli.cli, ["insert", "date", "newkey: value", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-date"))

    def test_insert_after_int(self):
        result = self.cli.invoke(cli.cli, ["insert", "invoice", "newkey: value", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-int"))

    def test_insert_after_float(self):
        result = self.cli.invoke(cli.cli, ["insert", "tax", "newkey: value", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-float"))

    def test_insert_after_string(self):
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-string"))
