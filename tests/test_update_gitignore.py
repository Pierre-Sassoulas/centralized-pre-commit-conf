import unittest

from centralized_pre_commit_conf.update_gitignore import get_updated_gitignore_content

GITIGNORE_INFO_TEXT = "# fervpierpvjepvjpvjepvjperjverpovpeorvpor"


class TestUpdateGitignore(unittest.TestCase):
    def test_nothing(self):
        text, mode = get_updated_gitignore_content("", set(["a", "b", "c"]), GITIGNORE_INFO_TEXT)
        self.assertEqual(mode, "a")
        self.assertEqual(
            text,
            f"""{GITIGNORE_INFO_TEXT}
a
b
c
""",
        )

    def test_something(self):
        text, mode = get_updated_gitignore_content("d\ne\n", set(["a", "b", "c"]), GITIGNORE_INFO_TEXT)
        self.assertEqual(mode, "a")
        self.assertEqual(
            text,
            f"""
{GITIGNORE_INFO_TEXT}
a
b
c
""",
        )

    def test_old_cppc_data(self):
        text, mode = get_updated_gitignore_content(
            f"d\ne\n{GITIGNORE_INFO_TEXT}\nf\ng\n", set(["a", "b", "c"]), GITIGNORE_INFO_TEXT
        )
        self.assertEqual(mode, "w")
        self.assertEqual(
            text,
            f"""d
e

{GITIGNORE_INFO_TEXT}
a
b
c
f
g
""",
        )

    def test_duplicated_old_cppc_data(self):
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
            set(["a", "b", "c"]),
            GITIGNORE_INFO_TEXT,
        )
        self.assertEqual(mode, "w")
        self.assertEqual(
            text,
            f"""d
e

{GITIGNORE_INFO_TEXT}
a
b
c
f
g

h
i
""",
        )

    def test_real_data(self):
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
            set([".clang-format", ".clang-tidy", ".csslintrc"]),
            GITIGNORE_INFO_TEXT,
        )
        self.assertEqual(mode, "w")
        self.assertEqual(
            text,
            f""".idea/
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
""",
        )
