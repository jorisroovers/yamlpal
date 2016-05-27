from yamlpal.tests.base import BaseTestCase
from yamlpal import cli
from click.testing import CliRunner


class InsertionTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_insert_inline(self):
        with self.copy_sample("sample1") as copy_path:
            result = self.cli.invoke(cli.cli, ["insert", "--inline", "title", "newkey: value", "-f", copy_path])
            actual = open(copy_path).read()
            self.assertEqual(result.output, "")
            self.assertEqual(actual, self.get_expected("sample1-after-string"))

    def test_insert_ignore_leading_trailing_whitespace(self):
        result = self.cli.invoke(cli.cli, ["insert", "title", "   newkey: value \t \n",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-string"))

    def test_insert_after_date(self):
        result = self.cli.invoke(cli.cli, ["insert", "date", "newkey: value", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-date"))

    def test_insert_after_int(self):
        result = self.cli.invoke(cli.cli, ["insert", "invoice", "newkey: value", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-int"))

    def test_insert_after_float(self):
        result = self.cli.invoke(cli.cli, ["insert", "tax", "newkey: value", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-float"))

    def test_insert_after_string(self):
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value", "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-after-string"))

    def test_into_dictionary(self):
        result = self.cli.invoke(cli.cli,
                                 ["insert", "bill-to/address", "newkey: value\n",
                                  "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-into-dictionary"))

    def test_into_list(self):
        # TODO(jroovers): this create invalid yaml. We need to do smart insertion!
        result = self.cli.invoke(cli.cli, ["insert", "product", "newkey: value\n",
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-into-list"))

    def test_multiple_file_flags(self):
        # default case: multiple file flags
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value",
                                           "-f", self.get_sample_path("sample1"),
                                           "-f", self.get_sample_path("sample2")])
        output1 = self.get_expected("sample1-after-string")
        output2 = self.get_expected("sample2-after-string")
        self.assertEqual(result.output, output1 + output2)

        # default case: swapped order -> yamlpal maintains the order
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value",
                                           "-f", self.get_sample_path("sample2"),
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, output2 + output1)

        # Same file 3 times (yamlpal does NOT select unique filepaths, it does exactly what you tell it to do)
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value",
                                           "-f", self.get_sample_path("sample1"),
                                           "-f", self.get_sample_path("sample1"),
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, output1 + output1 + output1)

    def test_multiple_stdin_files(self):
        # default case:  multiple files via stdin
        stdin = "%s\n%s" % (self.get_sample_path("sample1"), self.get_sample_path("sample2"))
        output1 = self.get_expected("sample1-after-string")
        output2 = self.get_expected("sample2-after-string")
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value"], input=stdin)
        self.assertEqual(result.output, output1 + output2)

        # default case: swapped order -> yamlpal maintains the order
        stdin = "%s\n%s" % (self.get_sample_path("sample2"), self.get_sample_path("sample1"))
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value"], input=stdin)
        self.assertEqual(result.output, output2 + output1)

        # combination of stdin and file flags
        stdin = "%s\n%s" % (self.get_sample_path("sample1"), self.get_sample_path("sample2"))
        output3 = self.get_expected("sample3-after-string")
        result = self.cli.invoke(cli.cli, ["insert", "title", "newkey: value",
                                           "-f", self.get_sample_path("sample1"),
                                           "-f", self.get_sample_path("sample3")],
                                 input=stdin)
        self.assertEqual(result.output, output1 + output3 + output1 + output2)

    def test_insert_content_from_file(self):
        result = self.cli.invoke(cli.cli, ["insert", "title", "@" + self.get_sample_path("insert-multiline.txt"),
                                           "-f", self.get_sample_path("sample1")])
        self.assertEqual(result.output, self.get_expected("sample1-multiline-insert"))
