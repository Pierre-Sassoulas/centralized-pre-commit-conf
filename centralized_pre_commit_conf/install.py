"""Install your centralized pre-commit configuration at the root of your local git workdir."""

import argparse
import os
import subprocess
import sys

import confuse
from centralized_pre_commit_conf.constants import APPLICATION_NAME
from centralized_pre_commit_conf.prints import error, info, success, warn
from centralized_pre_commit_conf.update_gitignore import update_gitignore


def main(argv=None):
    config = confuse.Configuration(APPLICATION_NAME, __name__)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=config["repository"].get(), help="Git repository URL")
    parser.add_argument("--branch", default=config["branch"].get("str"), help="Git branch")
    parser.add_argument("--path", default=config["path"].get(), help="Path inside the git repository")
    parser.add_argument("-f", "--replace-existing", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    config.set_args(args)
    url = get_url_from_args(args.url, args.branch, args.path)
    config_files = config["configuration_files"].get()
    if args.verbose:
        info(f"Installing with the following options : {config}")
        info(f"Configuration files to fetch : {config_files}.")
    install(url=url, config_files=config_files, replace_existing=args.replace_existing, verbose=args.verbose)


def get_url_from_args(url: str, branch: str, path: str) -> str:
    """Necessary because we don't want to have to handle redirection."""
    if url.endswith("/"):
        url = url[:-1]
    if path.endswith("/"):
        path = path[:-1]
    return f"{url}/{branch}/{path}"


def install(url, config_files, replace_existing=False, verbose=False):
    download_fail = 0
    download_success = 0
    for config_file in config_files:
        max_len = max(len(c) for c in config_files)
        if os.path.exists(config_file) and not replace_existing:
            formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
            warn(f"Found existing {formatted_config} ⁉️  Use '-f' or '--replace-existing' to force erase.")
            continue
        if download_configuration_file(f"{url}/{config_file}", config_file, max_len, verbose):
            download_success += 1
        else:
            download_fail += 1
    install_pre_commit = ["pip3", "install", "pre-commit==1.14.0"]
    if verbose:
        info(f"Launching : {install_pre_commit}")
    subprocess.run(install_pre_commit, capture_output=True)
    init_pre_commit = ["pre-commit", "install"]
    if verbose:
        info(f"Launching : {init_pre_commit}")
    subprocess.run(init_pre_commit, capture_output=True)
    update_gitignore(config_files, verbose)
    if download_fail == 0:
        if download_success > 0:
            plural = "s" if download_success > 1 else ""
            success(f" 🎉 {download_success} configuration file{plural} recovered and pre-commit installed correctly. 🎉")
        else:
            warn(f"All configuration files already existed.")
    else:
        pluralization = "s were" if download_fail != 1 else " was"
        warn(f" 🎻 {download_fail} configuration file{pluralization} not recovered correctly. 🎻")


def download_configuration_file(file_to_download, config_file, max_len, verbose):
    command = ["curl", "-O", file_to_download, "-f"]
    if verbose:
        info(f"Launching {command} to download {config_file}")
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        error_msg = f"download failed 💥 \n{result.stderr.decode('utf8')}"
        if result.returncode == 22:
            error_msg = "not found. Are you sure it exists ? 💥"
        error(f" 💥 '{file_to_download}' {error_msg}")
    else:
        formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
        success("✨ Successfully retrieved {} ✨".format(formatted_config))
    return result.returncode == 0


if __name__ == "__main__":
    sys.exit(main())
