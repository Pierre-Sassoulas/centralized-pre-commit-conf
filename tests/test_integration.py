import sys
import unittest
from typing import List

import pytest

from centralized_pre_commit_conf.main import run

URL = "https://raw.githubusercontent.com/Pierre-Sassoulas/centralized-pre-commit-conf"


@pytest.mark.vcr()
class TestIntegration(unittest.TestCase):
    def test_help(self):
        self.assert_exit_with_code(["pre-commit-conf", "-h"], 0)

    def test_bad_arg(self):
        self.assert_exit_with_code(["pre-commit-conf", "--not-exist"], 2)

    def test_normal_args(self):
        self.assert_exit_with_code(
            [
                "pre-commit-conf",
                "--repository",
                URL,
                "--branch",
                "master",
                "--path",
                "centralized_pre_commit_conf/static",
                "-f",
                "--insecure",
                "-vv",
            ],
            0,
        )

    def assert_exit_with_code(self, command: List[str], expected_code: int):
        sys.argv = command
        with self.assertRaises(SystemExit) as sys_exit:
            run()
        error_msg = f"{sys_exit} exited with the wrong error code ({sys_exit.exception.code}) for args: {command}"
        assert sys_exit.exception.code == expected_code, error_msg
