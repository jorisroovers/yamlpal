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
                                           "-F", "%{file} %{linenr} %{linenr.end} %{key} %{value}",
                                           "-f", sample_path])
        self.assertEqual(result.output, "%s 11 11 city Royal Oak\n" % sample_path)

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
        expected = 'address: {\n    "city": "Royal Oak", \n    "state": "MI", \n    "postal": "48046", \n    ' + \
                   '"lines": "458 Walkman Dr.\\nSuite #292\\n"\n}\n'
        self.assertEqual(result.output, expected)

    def test_find_list(self):
        result = self.cli.invoke(cli.cli, ["find", "product", "-f", self.get_sample_path("sample1")])
        expected = 'product: [\n    {\n        "sku": "BL394D", \n        "price": "450.0", \n        ' + \
                   '"description": "Basketball", \n        "quantity": "4"\n    }, \n    ' + \
                   '{\n        "sku": "BL4438H", \n        "price": "2392.0", \n        ' + \
                   '"description": "Super Hoop", \n        "quantity": "1"\n    }\n]\n'
        self.assertEqual(result.output, expected)

    def test_find_linenumbers(self):
        query_result_mapping = {
            'invoice': "2-2\n",
            'date': "3-3\n",
            'bill-to': "5-13\n",
            'bill-to/given': "5-5\n",
            'bill-to/family': "6-6\n",
            'bill-to/address': "8-13\n",
            'bill-to/address/lines': "8-10\n",
            'bill-to/address/city': "11-11\n",
            'bill-to/address/state': "12-12\n",
            'bill-to/address/postal': "13-13\n",
            # 'ship-to': "14-14\n", # TODO(jroovers): searching for references is not yet supported by yamlpal
            'product': "16-23\n",
            'product[0]': "16-19\n",
            'product[1]': "20-23\n",
            'product[0]/sku': "16-16\n",
            'product[0]/quantity': "17-17\n",
            'product[0]/description': "18-18\n",
            'product[0]/price': "19-19\n",
            'labels': "25-27\n",
            'tax': "28-28\n",
            'title': "29-29\n",
            'total': "30-30\n",
            # 'comments': "30-33\n", # TODO(jroovers): we don't correctly parse text that starts with > yet
        }
        for query, expected in query_result_mapping.iteritems():
            # Test line numbers
            result = self.cli.invoke(cli.cli, ["find", query, "-F", "%{linenr}-%{linenr.end}",
                                               "-f", self.get_sample_path("sample1")])

            self.assertEqual(result.output, expected, "%s: %s!=%s" % (query, result.output, expected))
