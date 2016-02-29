from unittest import TestCase

import os
import time
import shutil


class BaseTestCase(TestCase):
    # In case of assert failures, print the full error message
    maxDiff = None

    @staticmethod
    def get_sample_path(filename=""):
        samples_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "samples")
        _, ext = os.path.splitext(filename)
        if ext == '':
            filename += ".yml"
        return os.path.join(samples_dir, filename)

    @staticmethod
    def get_expected(filename=""):
        expected_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "expected")
        _, ext = os.path.splitext(filename)
        if ext == '':
            filename += ".yml"
        expected_path = os.path.join(expected_dir, filename)
        expected = open(expected_path).read()
        return expected

    @staticmethod
    def copy_sample(samplename):
        return TempSampleCopy(samplename)


class TempSampleCopy(object):
    """ Simple context manager that copies a given sample file and makes it path available in it's context.
        After exiting the context, the sample file copy is deleted."""

    def __init__(self, samplename):
        self.sample_path = BaseTestCase.get_sample_path(samplename)
        filename = os.path.basename(self.sample_path)
        copy_filename = "copy_%s_%s" % (filename, time.strftime("%Y-%m-%d-%H-%M-%S"))
        sample_dir = os.path.dirname(self.sample_path)
        self.copy_path = os.path.join(sample_dir, copy_filename)

    def __enter__(self):
        shutil.copyfile(self.sample_path, self.copy_path)
        return self.copy_path

    def __exit__(self, type, value, tb):
        os.remove(self.copy_path)
