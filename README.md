# Centralized `pre-commit` configuration

[![Build Status](https://travis-ci.org/Pierre-Sassoulas/centralized-pre-commit-conf.svg?branch=master)](https://travis-ci.org/Pierre-Sassoulas/centralized-pre-commit-conf)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/centralized-pre-commit-conf/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/centralized-pre-commit-conf?branch=master)
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

## Development / contribution

```bash
pip3 install -e ".[test]"
pre-commit-conf
python3 -m pytest --cov centralized_pre_commit_conf
```

Pull requests are welcome :)
