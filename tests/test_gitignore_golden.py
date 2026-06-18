"""Golden master tests for the .gitignore generation, including tool caches.

Each case directory under ``gitignore_cases`` holds:
- ``gitignore_in``    the existing .gitignore content (may be empty);
- ``config_files``    the installed configuration files, one per line;
- ``cache_files.json``  the config-file -> cache-entries mapping;
- ``expected.gitignore``  the golden output (regenerate with ``--remaster``).

The whole ``update_gitignore`` flow is exercised end to end, so the golden
files capture cache expansion *and* the deduplication of entries already
present in the .gitignore.
"""

import json
from pathlib import Path

import pytest
from pytest_remaster import CaseData, GoldenMaster, discover_test_cases

from centralized_pre_commit_conf.update_gitignore import update_gitignore

CASES_DIR = Path(__file__).parent / "gitignore_cases"
CASES = discover_test_cases(CASES_DIR)


@pytest.mark.parametrize("case", CASES)  # type: ignore[untyped-decorator]
def test_gitignore(case: CaseData, golden_master: GoldenMaster, tmp_path: Path) -> None:
    config_files = (case.input / "config_files").read_text().split()
    cache_files = json.loads((case.input / "cache_files.json").read_text())
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text((case.input / "gitignore_in").read_text())
    update_gitignore(config_files, False, cache_files, path=gitignore)
    golden_master.check(gitignore.read_text(), case.expected(suffix=".gitignore"))
