import unittest

from centralized_pre_commit_conf.update_gitignore import (
    get_gitignore_entries,
    get_updated_gitignore_content,
)

GITIGNORE_INFO_TEXT = "# fervpierpvjepvjpvjepvjperjverpovpeorvpor"


class TestGitignoreEntries(unittest.TestCase):
    def test_no_cache_files(self) -> None:
        assert get_gitignore_entries([".pylintrc"]) == {".pylintrc"}

    def test_cache_added(self) -> None:
        entries = get_gitignore_entries(
            ["mypy.ini", ".pylintrc"], {"mypy.ini": [".mypy_cache/"]}
        )
        assert entries == {"mypy.ini", ".pylintrc", ".mypy_cache/"}

    def test_cache_skipped_no_tool(self) -> None:
        entries = get_gitignore_entries([".pylintrc"], {"mypy.ini": [".mypy_cache/"]})
        assert entries == {".pylintrc"}

    def test_several_cache_entries(self) -> None:
        entries = get_gitignore_entries(
            ["tool.cfg"], {"tool.cfg": [".a_cache/", ".b_cache/"]}
        )
        assert entries == {"tool.cfg", ".a_cache/", ".b_cache/"}


class TestUpdateGitignore(unittest.TestCase):
    def test_nothing(self) -> None:
        text, mode = get_updated_gitignore_content(
            "", {"a", "b", "c"}, GITIGNORE_INFO_TEXT
        )
        assert mode == "a"
        assert text == f"""{GITIGNORE_INFO_TEXT}
a
b
c
"""

    def test_something(self) -> None:
        text, mode = get_updated_gitignore_content(
            "d\ne\n", {"a", "b", "c"}, GITIGNORE_INFO_TEXT
        )
        assert mode == "a"
        assert text == f"""
{GITIGNORE_INFO_TEXT}
a
b
c
"""

    def test_old_cppc_data(self) -> None:
        text, mode = get_updated_gitignore_content(
            f"d\ne\n{GITIGNORE_INFO_TEXT}\nf\ng\n", {"a", "b", "c"}, GITIGNORE_INFO_TEXT
        )
        assert mode == "w"
        assert text == f"""d
e

{GITIGNORE_INFO_TEXT}
a
b
c
f
g
"""

    def test_duplicated_old_cppc_data(self) -> None:
        text, mode = get_updated_gitignore_content(
            f"""d
e
{GITIGNORE_INFO_TEXT}
f
g

{GITIGNORE_INFO_TEXT}
h
i
""",
            {"a", "b", "c"},
            GITIGNORE_INFO_TEXT,
        )
        assert mode == "w"
        assert text == f"""d
e

{GITIGNORE_INFO_TEXT}
a
b
c
f
g

h
i
"""

    def test_real_data(self) -> None:
        text, mode = get_updated_gitignore_content(
            f""".idea/
*.egg-info/

{GITIGNORE_INFO_TEXT}
.isort.cfg
.pylintrc
.flake8
.pre-commit-config.yaml

build/
dist/
""",
            {".clang-format", ".clang-tidy", ".csslintrc"},
            GITIGNORE_INFO_TEXT,
        )
        assert mode == "w"
        assert text == f""".idea/
*.egg-info/


{GITIGNORE_INFO_TEXT}
.clang-format
.clang-tidy
.csslintrc
.isort.cfg
.pylintrc
.flake8
.pre-commit-config.yaml

build/
dist/
"""
