from yamlpal.tests.base import BaseTestCase
from click.testing import CliRunner


class FindNegativeTests(BaseTestCase):
    def setUp(self):
        self.cli = CliRunner()
