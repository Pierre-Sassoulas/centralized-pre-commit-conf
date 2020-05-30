import enum

APPLICATION_NAME = "pre-commit-conf"


class ExitCode(enum.Enum):
    OK = 0
    PRE_COMMIT_CONF_NOT_FOUND = 1
