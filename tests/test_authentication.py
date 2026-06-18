import requests

from centralized_pre_commit_conf.download_configuration import (
    _authentication_headers,
    is_successful_download,
)


class TestAuthenticationHeaders:
    def test_no_token(self) -> None:
        assert not _authentication_headers("")

    def test_with_token(self) -> None:
        assert _authentication_headers("secret") == {"PRIVATE-TOKEN": "secret"}


class TestIsSuccessfulDownload:
    def _response(
        self, status_code: int, history: list[requests.Response]
    ) -> requests.Response:
        response = requests.Response()
        response.status_code = status_code
        response.history = history
        response.url = "http://a.net/.flake8"
        return response

    def test_direct_200_is_success(self) -> None:
        assert is_successful_download(self._response(200, [])) is True

    def test_non_200_is_failure(self) -> None:
        assert is_successful_download(self._response(404, [])) is False

    def test_redirected_200_is_failure(self) -> None:
        # Login page redirection: 200 but content is HTML, not the raw file.
        redirect = self._response(302, [])
        assert is_successful_download(self._response(200, [redirect])) is False
