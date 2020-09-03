import sys
from pathlib import Path

import confuse

from centralized_pre_commit_conf.constants import APPLICATION_NAME, ExitCode
from centralized_pre_commit_conf.install import install
from centralized_pre_commit_conf.parse_args import parse_args
from centralized_pre_commit_conf.prints import error, info


def run():
    config = confuse.Configuration(APPLICATION_NAME, __name__)
    try:
        config = parse_args(config)
    except confuse.ConfigError as e:
        error(f"Problem with your configuration file in {[s.filename for s in config.sources]}: {e}")
        sys.exit(ExitCode.PRE_COMMIT_CONF_NOT_FOUND.value)
    config_path = Path(config.config_dir()).resolve() / "config.yaml"
    if not config_path.exists():
        info(f"You can set the option system wide in {config_path}.")
    if config["verbose"].get(bool):
        info(f"Installing with the following options : {config}.")
    install(config)
    sys.exit(ExitCode.OK.value)


if __name__ == "__main__":
    run()
