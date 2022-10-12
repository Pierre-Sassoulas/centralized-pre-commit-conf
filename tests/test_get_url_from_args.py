from centralized_pre_commit_conf.parse_args import get_url_from_args


class TestGetUrlFromArgs:
    def test_all_args(self) -> None:
        assert (
            get_url_from_args("http://a.net", "master", "path")
            == "http://a.net/master/path"
        )
        assert (
            get_url_from_args("http://a.net/", "master", "path")
            == "http://a.net/master/path"
        )
        assert (
            get_url_from_args("http://a.net", "master", "path/")
            == "http://a.net/master/path"
        )
        assert get_url_from_args("http://a.net", "master", "") == "http://a.net/master"
        assert get_url_from_args("http://a.net", "master", "/") == "http://a.net/master"
        assert get_url_from_args("http://a.net", "", "") == "http://a.net"
        assert get_url_from_args("http://a.net", "", "/") == "http://a.net"
        assert get_url_from_args("http://a.net", "", "path"), "http://a.net/path"
