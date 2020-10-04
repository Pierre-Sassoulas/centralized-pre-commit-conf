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
    parser.add_argument("-r", "--repository", default=config["repository"].get(), help="Git repository URL")
    parser.add_argument("-b", "--branch", default=config["branch"].get("str"), help="Git branch")
    parser.add_argument("-p", "--path", default=config["path"].get(), help="Path inside the git repository")
    default_replace = config["replace_existing"].get(bool)
    parser.add_argument(
        "-f", "--replace-existing", default=default_replace, action="store_true", help="Replace the existing file?"
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
        "-k", "--insecure", default=default_insecure, action="store_true", help="Accept self signed certificate?"
    )
    parser.add_argument("--no-replace-existing", dest="replace_existing", action="store_false")
    default_verbose = config["verbose"].get(bool)
    parser.add_argument(
        "-v", "--verbose", default=default_verbose, action="store_true", help="Display additional information?"
    )
    parser.add_argument("--no-verbose", dest="verbose", action="store_false")
    args = parser.parse_args()
    config.set_args(args)
    return config
