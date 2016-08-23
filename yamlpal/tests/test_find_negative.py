from yamlpal.tests.base import BaseTestCase
from click.testing import CliRunner
from yamlpal import cli


class FindNegativeTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_invalid_search_string(self):
        # non-existing key
        sample_path = self.get_sample_path("sample1")
        result = self.cli.invoke(cli.cli, ["find", "foobar", "-f", sample_path])
        self.assertEqual(result.output, "ERROR: Invalid search string 'foobar' for file '%s'\n" % sample_path)

        # non-existing child key
        result = self.cli.invoke(cli.cli, ["find", "bill-to/foo", "-f", sample_path])
        self.assertEqual(result.output, "ERROR: Invalid search string 'bill-to/foo' for file '%s'\n" % sample_path)

        # string where list index is expected
        result = self.cli.invoke(cli.cli, ["find", "product/bla", "-f", sample_path])
        self.assertEqual(result.output, "ERROR: Invalid search string 'product/bla' for file '%s'\n" % sample_path)

        # number as key where list index is expected
        result = self.cli.invoke(cli.cli, ["find", "product/0", "-f", sample_path])
        self.assertEqual(result.output, "ERROR: Invalid search string 'product/0' for file '%s'\n" % sample_path)
