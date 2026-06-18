# Centralized `pre-commit` configuration

[![PyPI version](https://badge.fury.io/py/centralized-pre-commit-conf.svg)](https://badge.fury.io/py/centralized-pre-commit-conf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Easily install and update centralized pre-commit hooks and their configuration files in
decentralized repositories.

To be able to validate and automatically fix commits we're using
[git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

We're also heavily relying on `pre-commit`, which is a framework for managing and
maintaining multi-language pre-commit hooks. Please refer to the
[pre-commit documentation here](https://pre-commit.com/).

## Philosophy

In order to be able to install all the tools and linters in a single command with up to
date centralized configurations, we're copying the configurations files of your tools
(`.pre-commit-config.yaml`, `isort.cfg`, `.flake8`, `.clang-format`, ...) from an URL to
your local git directory and we then install `pre-commit`.

Why not use only `pre-commit` by @asotile? Well,
[in his words](https://github.com/pre-commit/pre-commit/issues/450#issuecomment-405616722):

> pre-commit will not directly support mutability in configuration (this includes
> referencing a centralized repository). This causes lots of issues with repeatability
> and maintenance in general. This was an early design decision after seeing the pain
> caused at scale when a linter changes behaviour and suddenly every repository's master
> branch is broken.

So if you disagree and want decentralized repository with centralized lint
configuration, you need a tool on top of pre-commit to shoot yourself in the foot
anyway. Or more realistically to update your configuration files from a central
repository from time to time.

More seriously, the alternative is to use
[all-repos](https://github.com/asottile/all-repos) to mass update a bunch of
decentralized repositories with a decentralized configuration.

## Installation

```bash
pip3 install centralized-pre-commit-conf
```

## Usage

See `pre-commit-conf --help` for options.

### Installing hooks

For example with this `config.yaml` in
[one of the appropriate search paths](https://confuse.readthedocs.io/en/latest/#search-paths):

```yaml
configuration_files:
  - ".pylintrc"
  - ".pre-commit-config.yaml"
repository: https://mycompany.net/lint-conf/
branch: master
update_gitignore: True
path: "pre-commit/static/"
gitignore_info_text:
  "# Configuration file added automatically by 'centralized-pre-commit-conf'"
```

`pre-commit-conf` would recover the defined configuration files from
`https://mycompany.net/lint-conf/master/pre-commit/static/` and update the `.gitignore`:

```bash
You can set the option system wide in /home/pierre/.config/pre-commit-conf/config.yaml.
✨ Successfully retrieved .pre-commit-config.yaml ✨
✨ Successfully retrieved .pylintrc               ✨
✨ Updated .gitignore successfully with {'.pre-commit-config.yaml', '.pylintrc'}. ✨
 🎉 2 configuration files recovered and pre-commit installed correctly. 🎉
```

Here would the content of the `.gitignore`:

```ini
# Configuration file added automatically by 'centralized-pre-commit-conf'
.pre-commit-config.yaml
.pylintrc
```

### Ignoring tool cache files

Some tools write a cache to the work directory (`mypy` creates `.mypy_cache/`, `pytest`
creates `.pytest_cache/`, `ruff` creates `.ruff_cache/`, ...). These caches can be added
to the `.gitignore` automatically. `cache_files` maps a tool's configuration file to the
cache entries it generates; when that configuration file is installed and
`update_gitignore` is on, its cache entries are added to the `.gitignore` alongside the
configuration file:

```yaml
configuration_files:
  - "mypy.ini"
  - ".pre-commit-config.yaml"
update_gitignore: True
cache_files:
  "mypy.ini": [".mypy_cache/"]
```

resulting in:

```ini
# Configuration file added automatically by 'centralized-pre-commit-conf'
.mypy_cache/
.pre-commit-config.yaml
mypy.ini
```

The default configuration already maps `mypy`, `pytest` and `ruff`. Add your own tools
by extending `cache_files`.

Then with the same configuration, using `pre-commit-conf --branch hardcore-pylint-conf`
would try to recover the configuration files from
`https://mycompany.net/lint-conf/hardcore-pylint-conf/pre-commit/static/` instead.

```bash
You can set the option system wide in /home/pierre/.config/pre-commit-conf/config.yaml.
Found existing .pre-commit-config.yaml ⁉️  Use '-f' or '--replace-existing' to force erase.
Found existing .pylintrc               ⁉️  Use '-f' or '--replace-existing' to force erase.
All configuration files already existed.
```

Next commit supposing the `.pre-commit-config.yaml` is done correctly your modified
files we be linted with the centralized configuration.

### Private repositories (authentication)

If your configuration lives in a private repository, an unauthenticated request is
redirected to a login page and the HTML of that page would be downloaded instead of your
configuration file. `pre-commit-conf` detects that redirection and reports a failed
download asking you to provide a token.

To authenticate, provide a token. The token is sent as the `PRIVATE-TOKEN` header on
every request.

You do **not** need a broad token: `pre-commit-conf` only reads from the single
repository that holds your centralized configuration, so grant the least privilege that
works. On GitLab, prefer a
[Project Access Token](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)
created on that one configuration repository, with only the `read_repository` scope. A
Group Access Token (if the configuration repository may move within a group) or a
Personal Access Token also work, but a Personal Access Token can read every repository
your account can access — if it leaks, everything leaks — so avoid it unless necessary.

On GitLab, set `provider: gitlab`. The `read_repository` scope authenticates against the
[Repository Files API](https://docs.gitlab.com/ee/api/repository_files.html), not the
`/-/raw/` web endpoint (which only accepts a browser session), so `pre-commit-conf`
fetches each file through the API. Point `repository` at the project's web URL — the
host and project path are enough, the API URL is built for you:

```yaml
configuration_files:
  - ".pylintrc"
  - ".pre-commit-config.yaml"
repository: https://gitlab.mycompany.net/admin-sys/internal-pre-commit-conf
provider: gitlab
branch: master
path: ""
```

Then supply the token using one of the following (precedence: CLI > config > env var — a
`token` set in a config file shadows the environment variable):

1. **Environment variable (recommended)** — set it once, used on every run, never stored
   in a committed file:

   ```bash
   export PRE_COMMIT_CONF_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
   pre-commit-conf
   ```

2. **Config file** — convenient but keep the file out of version control, it contains a
   secret:

   ```yaml
   token: "glpat-xxxxxxxxxxxxxxxxxxxx"
   ```

3. **Command line** — avoid for real tokens, it leaks into your shell history and the
   process list:

   ```bash
   pre-commit-conf --token "glpat-xxxxxxxxxxxxxxxxxxxx"
   ```

In CI, store the token as a masked/protected variable named `PRE_COMMIT_CONF_TOKEN`.

Setup is a one-time thing: configure the repository once and keep the token available
(in your shell profile or CI secrets) so every run authenticates automatically. The only
recurring task is renewing the token when it expires.

## Development / contribution

```bash
pip3 install -e ".[test]"
pre-commit-conf
python3 -m pytest --cov centralized_pre_commit_conf
```

Pull requests are welcome :)
