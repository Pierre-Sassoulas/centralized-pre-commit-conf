# Centralized `pre-commit` configuration

Makes it possible to easily install and update pre-commit hooks, and
to centralize the configuration files of your tools.

To be able to validate and automatically fix commits we're using
[git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
and [pre-commit](https://pre-commit.com/). `pre-commit` is a framework
for managing and maintaining multi-language pre-commit hooks. The
`pre-commit` configuration file is `.pre-commit-config.yaml`.

## Philosophy

We don't want tools to be black boxes hidden inside the hooks. So in
order for tools to be used independently, we're copying the configurations
files (`isort.cfg`, `.flake8`, `.clang-format`, ...) in your git directory.

The idea is to be able to have multiple repository and to be able to
install all the tools and linters in a single command in each of them.

## Installation

Requirements :
  * Python 3.6 (black requires python 3.6)
  * curl
  * python3-pip
  * Connectivity to the central repository with your configuration files
  * ([pre-commit](https://pre-commit.com/) for the one line install to work)

**NB** : The hooks are going to be usable offline after installation

### One line install

If you trust the repository (ie: if you are me, no exception), you can
do a one line installation from scratch :
```bash
curl https://raw.githubusercontent.com/Pierre-Sassoulas/centralized-pre-commit-conf/master/centralized_pre_commit_conf/install.py|python3
```

Or, alternatively, if you're not me, you can fork the repository. Make
sure the `install.py` script is safe to use, and adapt the command and
configuration files for your fork.

### Advanced install

```bash
curl -O https://raw.githubusercontent.com/Pierre-Sassoulas/centralized-pre-commit-conf/master/centralized_pre_commit_conf/install.py
python3 install.py --help
```

### Installation without downloading anything from the internet

TODO

## What does this do ?

* Check the file you added before you commit
* Fix automatically what can be fixed
* You can then check and add the files that have been fixed
* If a hook is wrong you can bypass it. For example if you
want to skip pylint :

```bash
SKIP=pylint git commit -m "foo"
```
* You can run the hooks on all the files in the repository with :

```bash
pre-commit run --all-files
```

* Or only on some file(s) with:

```bash
pre-commit run --files somedir/*.py
```

* If you want to update the hooks you can do :

```bash
pre-commit autoupdate
```

You can then commit the resulting `.pre-commit-config.yaml`
to your fork's master branch so everyone benefit.

## Maintenance

### Creating a new hook

Before rushing to implement something, search for a hook coded by someone else.
If you need to create one you can add it inside the repository.
See [the pre-commit documentation here](https://pre-commit.com/).
