from unittest import TestCase


class BaseTestCase(TestCase):
    # In case of assert failures, print the full error message
    maxDiff = None
