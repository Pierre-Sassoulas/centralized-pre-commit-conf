# Centralized `pre-commit` configuration

[![Build Status](https://travis-ci.org/Pierre-Sassoulas/centralized-pre-commit-conf.svg?branch=master)](https://travis-ci.org/Pierre-Sassoulas/centralized-pre-commit-conf)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/centralized-pre-commit-conf/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/centralized-pre-commit-conf?branch=master)
[![PyPI version](https://badge.fury.io/py/centralized-pre-commit-conf.svg)](https://badge.fury.io/py/centralized-pre-commit-conf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Easily install and update centralized pre-commit hooks and their
configuration files in decentralized repositories.

To be able to validate and automatically fix commits we're using
[git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

We're also heavily relying on `pre-commit`, which is a framework for managing
and maintaining multi-language pre-commit hooks. Please refer to the
[pre-commit documentation here](https://pre-commit.com/).

## Philosophy

In order to be able to install all the tools and linters in a single
command with up to date configuration, we're copying the configurations
files of your tools (`.pre-commit-config.yaml`, `isort.cfg`, `.flake8`,
 `.clang-format`, ...) from an URL to your local git directory and we
 then install `pre-commit`.

## Installation

```bash
pip3 install centralized-pre-commit-conf
pre-commit-conf --help
```

##  Usage

### Installing hooks

For example with this `config.yaml` in [one of the appropriate
search paths](https://confuse.readthedocs.io/en/latest/#search-paths):

```
configuration_files :
    - ".pylintrc"
    - ".pre-commit-config.yaml"
repository: https://mycompany.net/lint-conf/
branch: master
path: "pre-commit/static/"
gitignore_info_text: "# Configuration file added automatically by 'centralized-pre-commit-conf'"
```

`pre-commit-conf` would recover the defined configuration files from
`https://mycompany.net/lint-conf/master/pre-commit/static/` and update the `.gitignore`:

```
✨ Successfully retrieved .pre-commit-config.yaml ✨
✨ Successfully retrieved .pylintrc               ✨
✨ Updated .gitignore successfully with {'.pre-commit-config.yaml', '.pylintrc'}. ✨
 🎉 2 configuration files recovered and pre-commit installed correctly. 🎉
```

Here would the content of the `.gitignore`:
```
# Configuration file added automatically by 'centralized-pre-commit-conf'
.pre-commit-config.yaml
.pylintrc
```

Then with the same configuration, using `pre-commit-conf --branch hardcore-pylint-conf` would try to recover
the configuration files from `https://mycompany.net/lint-conf/hardcore-pylint-conf/pre-commit/static/` instead.

```
Found existing .pre-commit-config.yaml ⁉️  Use '-f' or '--replace-existing' to force erase.
Found existing .pylintrc               ⁉️  Use '-f' or '--replace-existing' to force erase.
All configuration files already existed.
```

Next commit supposing the `.pre-commit-config.yaml` is done correctly
your modified files we be linted with the centralized configuration.
