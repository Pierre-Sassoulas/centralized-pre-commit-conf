import sys
from pathlib import Path

import confuse

from centralized_pre_commit_conf.constants import APPLICATION_NAME, ExitCode
from centralized_pre_commit_conf.install import install
from centralized_pre_commit_conf.parse_args import get_url_from_args, parse_args
from centralized_pre_commit_conf.prints import error, info


def run():
    config = confuse.Configuration(APPLICATION_NAME, __name__)
    try:
        config = parse_args(config)
    except confuse.ConfigError as e:
        error(f"Problem with your configuration file in {[s.filename for s in config.sources]}: {e}")
        sys.exit(ExitCode.PRE_COMMIT_CONF_NOT_FOUND.value)
    url = get_url_from_args(config["repository"].get(str), config["branch"].get(str), config["path"].get(str))
    config_files = config["configuration_files"].get(list)
    verbose = config["verbose"].get(bool)
    replace_existing = config["replace_existing"].get(bool)
    insecure = config["insecure"].get(bool)
    update_gitignore_on_install = config["update_gitignore"].get(bool)
    config_path = Path(config.config_dir()).resolve() / "config.yaml"
    if not config_path.exists():
        info(f"You can set the option system wide in {config_path}.")
    if verbose:
        info(f"Installing with the following options : {config}.")
        info(f"Configuration files to fetch : {config_files}.")
    install(
        url=url,
        config_files=config_files,
        replace_existing=replace_existing,
        verbose=verbose,
        insecure=insecure,
        update_gitignore_on_install=update_gitignore_on_install,
    )
    sys.exit(ExitCode.OK.value)


if __name__ == "__main__":
    run()
