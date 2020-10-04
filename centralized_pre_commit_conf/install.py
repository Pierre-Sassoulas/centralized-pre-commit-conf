"""Install your centralized pre-commit configuration at the root of your local git workdir."""

import subprocess
import sys
from pathlib import Path
from typing import List

import confuse

from centralized_pre_commit_conf.constants import ExitCode
from centralized_pre_commit_conf.download_configuration import download_configuration
from centralized_pre_commit_conf.prints import info, success, warn
from centralized_pre_commit_conf.update_gitignore import update_gitignore


def install(config: confuse.Configuration) -> None:
    config_files = config["configuration_files"].get(list)
    verbose = config["verbose"].get(bool)
    download_configuration(config)
    install_pre_commit(verbose)
    if config["update_gitignore"].get(bool):
        update_gitignore(config_files, verbose)


def subprocess_compat_mode(commands: List[str]) -> subprocess.CompletedProcess:
    should_raise = False
    if sys.version_info.minor >= 7:
        return subprocess.run(commands, capture_output=True, check=should_raise)
    # python < 3.7
    return subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=should_raise)


def install_pre_commit(verbose: bool) -> None:
    if not Path(".pre-commit-config.yaml").exists():
        warn("No '.pre-commit-config.yaml' found, we can't install pre-commit.")
        sys.exit(ExitCode.PRE_COMMIT_CONF_NOT_FOUND)
    init_pre_commit = ["pre-commit", "install"]
    if verbose:
        info(f"Launching : {init_pre_commit}")
    subprocess_compat_mode(init_pre_commit)
    success("🎉 pre-commit installed locally with the current configuration. 🎉")
