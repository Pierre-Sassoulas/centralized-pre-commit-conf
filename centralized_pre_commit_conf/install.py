"""Install your centralized pre-commit configuration at the root of your local git workdir."""

import argparse
import os
import subprocess
import sys

from centralized_pre_commit_conf.configuration import CONFIG_FILES, DEFAULT_BRANCH, DEFAULT_PATH, DEFAULT_REPOSITORY
from centralized_pre_commit_conf.prints import error, info, success, warn


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_REPOSITORY, help="Git repository URL")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Git branch")
    parser.add_argument("--path", default=DEFAULT_PATH, help="Path inside the git repository")
    parser.add_argument("-f", "--replace-existing", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    if args.verbose:
        info(f"Installing with the following options : {args}")
        info(f"Configuration files to fetch : {CONFIG_FILES}.")
    download_fail = 0
    for config_file in CONFIG_FILES:
        if os.path.exists(config_file):
            if not args.replace_existing:
                warn(f"'{config_file}' already exists (use -f or --replace-existing to replace).")
                continue
        if download_configuration_file(args, config_file) != 0:
            download_fail += 1
    install_pre_commit = ["pip3", "install", "pre-commit==1.14.0"]
    if args.verbose:
        info(f"Launching : {install_pre_commit}")
    subprocess.run(install_pre_commit, capture_output=True)
    init_pre_commit = ["pre-commit", "install"]
    if args.verbose:
        info(f"Launching : {init_pre_commit}")
    subprocess.run(init_pre_commit, capture_output=True)
    if download_fail == 0:
        success(" 🎉 Configuration files recovered and pre-commit installed correctly. 🎉")
    else:
        warn(f"{download_fail} among {len(CONFIG_FILES)} configuration files were not recovered correctly.")


def download_configuration_file(args, config_file):
    file_to_download = f"{args.url}/{args.branch}/{args.path}/{config_file}"
    command = ["curl", "-O", file_to_download, "-f"]
    if args.verbose:
        info(f"Launching {command} to download {config_file}")
    result = subprocess.run(command, capture_output=True)
    if result.returncode == 22:
        error(f"'{file_to_download}' not found. Are you sure it exists ?")
    elif result.returncode != 0:
        error(f"'{file_to_download}' download failed:\n{result.stderr.decode('utf8')}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
