import sys
from typing import List

import pytest

from centralized_pre_commit_conf.main import run

URL = "https://raw.githubusercontent.com/Pierre-Sassoulas/centralized-pre-commit-conf"


@pytest.mark.vcr()
class TestIntegration:
    def test_help(self) -> None:
        self.assert_exit_with_code(["pre-commit-conf", "-h"], 0)

    def test_bad_arg(self) -> None:
        self.assert_exit_with_code(["pre-commit-conf", "--not-exist"], 2)

    def test_normal_args(self) -> None:
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

    def assert_exit_with_code(self, command: List[str], expected_code: int) -> None:
        sys.argv = command
        with pytest.raises(SystemExit) as sys_exit:
            run()
        error_msg = (
            f"{sys_exit} exited with the wrong error code "
            f"({sys_exit.value.code}) for args: {command}"
        )
        assert sys_exit.value.code == expected_code, error_msg
