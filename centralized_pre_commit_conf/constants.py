import enum

APPLICATION_NAME = "pre-commit-conf"
TIMEOUT = 10.0
# Token can also be supplied via this environment variable to avoid storing
# secrets in the config file or shell history.
TOKEN_ENV_VAR = "PRE_COMMIT_CONF_TOKEN"
# Supported ways to build download URLs. 'raw' templates the URL directly
# (GitHub raw and similar); 'gitlab' uses the Repository Files API.
PROVIDERS = ("raw", "gitlab")


class ExitCode(enum.Enum):
    OK = 0
    PRE_COMMIT_CONF_NOT_FOUND = 1
