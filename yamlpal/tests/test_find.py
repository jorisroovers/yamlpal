from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class FindTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_find_simple(self):
        result = self.cli.invoke(cli.cli, ["find", "title", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "title: Invoice for purchases\n")

    def test_find_number(self):
        result = self.cli.invoke(cli.cli, ["find", "tax", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "tax: 251.42\n")

    def test_find_complex(self):
        result = self.cli.invoke(cli.cli, ["find", "bill-to/address/city", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "city: Royal Oak\n")

    def test_find_custom_format(self):
        sample_path = self.get_sample_path("sample1")
        result = self.cli.invoke(cli.cli, ["find", "bill-to/address/city",
                                           "-F", "%{file} %{linenr} %{key} %{value}",
                                           "-f", sample_path])
        self.assertEqual(result.output, "%s 11 city Royal Oak\n" % sample_path)

    def test_find_custom_format_literal(self):
        result = self.cli.invoke(cli.cli, ["find", "bill-to/address/city",
                                           "-F", "%{literal}",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "        city    : Royal Oak\n")

    def test_find_key_of_list_item(self):
        result = self.cli.invoke(cli.cli, ["find", "labels[0]",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, "0: premium customer\n")

        result = self.cli.invoke(cli.cli, ["find", "labels[1]",
                                           "-f", self.get_sample_path("sample1")])

        self.assertEqual(result.output, "1: online order\n")
