CONFIG_FILES = [".flake8", ".isort.cfg", ".pre-commit-config.yaml", ".pylintrc"]
DEFAULT_REPOSITORY = "https://raw.githubusercontent.com/Pierre-Sassoulas/centralized-pre-commit-conf"
DEFAULT_BRANCH = "master"
DEFAULT_PATH = "centralized_pre_commit_conf/static"
DEPENDENCIES = ["black==19.3b0", "isort==4.3.15", "pylint", "flake8"]
GITIGNORE_INFO_TEXT = "# Configuration file added automatically by 'centralized-pre-commit-conf'"
