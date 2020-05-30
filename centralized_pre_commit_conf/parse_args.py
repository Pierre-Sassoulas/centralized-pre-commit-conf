import argparse

import confuse


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


def parse_args(config) -> confuse.Configuration:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=config["repository"].get(), help="Git repository URL")
    parser.add_argument("--branch", default=config["branch"].get("str"), help="Git branch")
    parser.add_argument("--path", default=config["path"].get(), help="Path inside the git repository")
    parser.add_argument(
        "-f",
        "--replace-existing",
        default=config["replace_existing"].get(bool),
        action="store_true",
        help="Replace the existing file?",
    )
    parser.add_argument("--no-replace-existing", dest="replace_existing", action="store_false")
    parser.add_argument(
        "-v",
        "--verbose",
        default=config["verbose"].get(bool),
        action="store_true",
        help="Display additional information?",
    )
    parser.add_argument("--no-verbose", dest="verbose", action="store_false")
    args = parser.parse_args()
    config.set_args(args)
    return config
