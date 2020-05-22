# Centralized `pre-commit` configuration

Makes it possible to easily install and update pre-commit hooks, and
to centralize the configuration files of your tools.

To be able to validate and automatically fix commits we're using
[git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
and [pre-commit](https://pre-commit.com/). `pre-commit` is a framework for managing and
maintaining multi-language pre-commit hooks. The `pre-commit` configuration file
is `.pre-commit-config.yaml`.

## Philosophy

We don't want tools to be black boxes hidden inside the hooks. So in
order for tools to be used independently, we're copying the configurations
files (`isort.cfg`, `.flake8`, `.clang-format`, ...) in your git directory.

The idea is to be able to have multiple repository and to be able to
install all the tools and linters in a single command.
