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

    def test_find_dictionary(self):
        result = self.cli.invoke(cli.cli, ["find", "bill-to/address", "-f", self.get_sample_path("sample1")])
        expected = '{\n    "city": "Royal Oak", \n    "state": "MI", \n    "postal": "48046", \n    ' + \
                   '"lines": "458 Walkman Dr.\\nSuite #292\\n"\n}\n'
        self.assertEqual(result.output, expected)

    def test_find_list(self):
        result = self.cli.invoke(cli.cli, ["find", "product", "-f", self.get_sample_path("sample1")])
        expected = '[\n    {\n        "sku": "BL394D", \n        "price": "450.0", \n        ' + \
                   '"description": "Basketball", \n        "quantity": "4"\n    }, \n    ' + \
                   '{\n        "sku": "BL4438H", \n        "price": "2392.0", \n        ' + \
                   '"description": "Super Hoop", \n        "quantity": "1"\n    }\n]\n'
        self.assertEqual(result.output, expected)
