"""Install your centralized pre-commit configuration at the root of your local git workdir."""

import subprocess
import sys
from pathlib import Path

from centralized_pre_commit_conf.constants import ExitCode
from centralized_pre_commit_conf.download_configuration import download_configuration
from centralized_pre_commit_conf.prints import info, success, warn
from centralized_pre_commit_conf.update_gitignore import update_gitignore


def install(url, config_files, replace_existing=False, verbose=False, insecure=False):
    download_configuration(config_files, replace_existing, url, verbose, insecure)
    install_pre_commit(verbose)
    update_gitignore(config_files, verbose)


def install_pre_commit(verbose):
    if not Path(".pre-commit-config.yaml").exists():
        warn("No '.pre-commit-config.yaml' found, we can't install pre-commit.")
        sys.exit(ExitCode.PRE_COMMIT_CONF_NOT_FOUND)
    install_pre_commit_command = ["pip3", "install", "pre-commit==1.14.0"]
    if verbose:
        info(f"Launching : {install_pre_commit_command}")
    subprocess.run(install_pre_commit_command, capture_output=True)
    init_pre_commit = ["pre-commit", "install"]
    if verbose:
        info(f"Launching : {init_pre_commit}")
    subprocess.run(init_pre_commit, capture_output=True)
    success(f"🎉 pre-commit installed locally with the current configuration. 🎉")
