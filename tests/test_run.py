import sys
import unittest
import os

sys.path.append("..")

import run
from cats_tools import buildFile


class TestRun(unittest.TestCase):
    def test_is_static_test_complete(self):
        self.assertEqual(run.is_static_test_complete(["1.in", "1.out"]), True)
        self.assertEqual(run.is_static_test_complete(["1.in"]), False)
        self.assertEqual(run.is_static_test_complete(["1.i", "1.out"]), False)

    def test_getting_runtime(self):
        test = run.StaticTest("1/pass", "/Users/chupson/dev/CATS/tests/std-test.exe",
                              "/Users/chupson/dev/CATS/tests/std-test_tests/1/pass.in",
                              "/Users/chupson/dev/CATS/tests/std-test_tests/1/pass.out")
        test.runtime_in_secs = 0.4458272835
        self.assertEqual("0.4458", test.get_runtime())
        test.runtime_in_secs = None
        self.assertEqual("unknown", test.get_runtime())

    def test_failing(self):
        self.assertEqual(True, False)

