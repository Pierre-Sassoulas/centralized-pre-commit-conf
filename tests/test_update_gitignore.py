import unittest

from centralized_pre_commit_conf.configuration import GITIGNORE_INFO_TEXT
from centralized_pre_commit_conf.update_gitignore import get_updated_gitignore_content


class TestUpdateGitignore(unittest.TestCase):
    def test_nothing(self):
        text, mode = get_updated_gitignore_content("", set(["a", "b", "c"]))
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
        text, mode = get_updated_gitignore_content("d\ne\n", set(["a", "b", "c"]))
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
