import argparse
from urllib.parse import quote, urlsplit

import confuse

from centralized_pre_commit_conf.constants import PROVIDERS, TOKEN_ENV_VAR


def get_url_from_args(url: str, branch: str, path: str) -> str:
    """Necessary because we don't want to have to handle redirection."""
    if url.endswith("/"):
        url = url[:-1]
    if path.endswith("/"):
        path = path[:-1]
    if path and branch:
        return f"{url}/{branch}/{path}"
    if branch:
        return f"{url}/{branch}"
    if path:
        return f"{url}/{path}"
    return f"{url}"


def build_config_file_url(
    provider: str, repository: str, branch: str, path: str, config_file: str
) -> str:
    """Build the download URL for a single configuration file.

    The default 'raw' provider templates the URL directly (e.g. GitHub raw).
    The 'gitlab' provider uses the Repository Files API, the only endpoint that
    a 'read_repository' token can authenticate to with the 'PRIVATE-TOKEN'
    header (the '/-/raw/' web endpoint requires a browser session).
    """
    if provider == "gitlab":
        return _gitlab_file_url(repository, branch, path, config_file)
    return f"{get_url_from_args(repository, branch, path)}/{config_file}"


def _gitlab_file_url(repository: str, branch: str, path: str, config_file: str) -> str:
    split = urlsplit(repository.rstrip("/"))
    host = f"{split.scheme}://{split.netloc}"
    project = split.path.strip("/")
    file_path = "/".join(part for part in (path.strip("/"), config_file) if part)
    return (
        f"{host}/api/v4/projects/{quote(project, safe='')}"
        f"/repository/files/{quote(file_path, safe='')}/raw?ref={branch}"
    )


def parse_args(config: confuse.Configuration) -> confuse.Configuration:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-r",
        "--repository",
        default=config["repository"].get(),
        help="Git repository URL",
    )
    parser.add_argument(
        "-b", "--branch", default=config["branch"].get(str), help="Git branch"
    )
    parser.add_argument(
        "-t",
        "--token",
        default=config["token"].get(str),
        help=(
            "Token to authenticate to a private repository "
            "(GitLab 'PRIVATE-TOKEN'). Can also be set via the "
            f"{TOKEN_ENV_VAR} environment variable."
        ),
    )
    parser.add_argument(
        "--provider",
        choices=PROVIDERS,
        default=config["provider"].get(str),
        help=(
            "How to build download URLs. 'raw' templates the URL directly "
            "(e.g. GitHub raw); 'gitlab' uses the Repository Files API so a "
            "'read_repository' token can authenticate to a private project."
        ),
    )
    parser.add_argument(
        "-p",
        "--path",
        default=config["path"].get(),
        help="Path inside the git repository",
    )
    default_replace = config["replace_existing"].get(bool)
    parser.add_argument(
        "-f",
        "--replace-existing",
        default=default_replace,
        action="store_true",
        help="Replace the existing file?",
    )
    parser.add_argument(
        "-c",
        "--configuration-files",
        nargs="+",
        help="Configuration files to fetch",
        default=config["configuration_files"].get(list),
    )
    update_gitignore = config["update_gitignore"].get(bool)
    parser.add_argument(
        "-u",
        "--update-gitignore",
        default=update_gitignore,
        action="store_true",
        help="Add configuration file to the .gitignore.",
    )
    default_insecure = config["insecure"].get(bool)
    parser.add_argument(
        "-k",
        "--insecure",
        default=default_insecure,
        action="store_true",
        help="Accept self signed certificate?",
    )
    parser.add_argument(
        "--no-replace-existing", dest="replace_existing", action="store_false"
    )
    default_verbose = config["verbose"].get(bool)
    parser.add_argument(
        "-v",
        "--verbose",
        default=default_verbose,
        action="store_true",
        help="Display additional information?",
    )
    parser.add_argument("--no-verbose", dest="verbose", action="store_false")
    args = parser.parse_args()
    config.set_args(args)
    return config
