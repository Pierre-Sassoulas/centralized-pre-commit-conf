from centralized_pre_commit_conf.parse_args import build_config_file_url


class TestBuildConfigFileUrl:
    def test_raw_provider_templates_url(self) -> None:
        assert (
            build_config_file_url(
                "raw",
                "https://raw.githubusercontent.com/owner/repo",
                "master",
                "static",
                ".flake8",
            )
            == "https://raw.githubusercontent.com/owner/repo/master/static/.flake8"
        )

    def test_raw_provider_without_path(self) -> None:
        assert (
            build_config_file_url(
                "raw", "https://a.net/owner/repo", "main", "", ".pylintrc"
            )
            == "https://a.net/owner/repo/main/.pylintrc"
        )

    def test_gitlab_provider_uses_files_api(self) -> None:
        assert build_config_file_url(
            "gitlab",
            "https://gitlab.e-lum.io/admin-sys/internal-pre-commit-conf",
            "master",
            "",
            ".pre-commit-config.yaml",
        ) == (
            "https://gitlab.e-lum.io/api/v4/projects/"
            "admin-sys%2Finternal-pre-commit-conf/repository/files/"
            ".pre-commit-config.yaml/raw?ref=master"
        )

    def test_gitlab_provider_encodes_path_and_trailing_slash(self) -> None:
        assert build_config_file_url(
            "gitlab",
            "https://gitlab.e-lum.io/group/sub/project/",
            "main",
            "configs/lint",
            ".flake8",
        ) == (
            "https://gitlab.e-lum.io/api/v4/projects/"
            "group%2Fsub%2Fproject/repository/files/"
            "configs%2Flint%2F.flake8/raw?ref=main"
        )
