from yamlpal.tests.base import BaseTestCase
from click.testing import CliRunner


class InsertionNegativeTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()
