from unittest import TestCase

import os


class BaseTestCase(TestCase):
    # In case of assert failures, print the full error message
    maxDiff = None

    @staticmethod
    def get_sample_path(filename=""):
        samples_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "samples")
        return os.path.join(samples_dir, filename + ".yml")

    @staticmethod
    def get_expected(filename=""):
        expected_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "expected")
        expected_path = os.path.join(expected_dir, filename + ".yml")
        expected = open(expected_path).read()
        return expected
