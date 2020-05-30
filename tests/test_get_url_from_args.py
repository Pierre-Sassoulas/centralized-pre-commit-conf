import unittest

from centralized_pre_commit_conf.parse_args import get_url_from_args


class TestGetUrlFromArgs(unittest.TestCase):
    def test_all_args(self):
        self.assertEqual(get_url_from_args("http://a.net", "master", "path"), "http://a.net/master/path")
        self.assertEqual(get_url_from_args("http://a.net/", "master", "path"), "http://a.net/master/path")
        self.assertEqual(get_url_from_args("http://a.net", "master", "path/"), "http://a.net/master/path")
        self.assertEqual(get_url_from_args("http://a.net", "master", ""), "http://a.net/master")
        self.assertEqual(get_url_from_args("http://a.net", "master", "/"), "http://a.net/master")
        self.assertEqual(get_url_from_args("http://a.net", "", ""), "http://a.net")
        self.assertEqual(get_url_from_args("http://a.net", "", "/"), "http://a.net")
        self.assertEqual(get_url_from_args("http://a.net", "", "path"), "http://a.net/path")
