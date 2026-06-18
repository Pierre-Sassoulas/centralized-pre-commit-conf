import os
from collections.abc import Iterable, Mapping
from pathlib import Path

import confuse

from centralized_pre_commit_conf.constants import APPLICATION_NAME
from centralized_pre_commit_conf.prints import info, success, warn


def get_gitignore_entries(
    config_files: Iterable[str],
    cache_files: Mapping[str, Iterable[str]] | None = None,
) -> set[str]:
    """Configuration files plus the cache entries of the tools they configure."""
    cache_files = cache_files or {}
    entries = set(config_files)
    for config_file in config_files:
        entries.update(cache_files.get(config_file, []))
    return entries


def update_gitignore(
    config_files: Iterable[str],
    verbose: bool,
    cache_files: Mapping[str, Iterable[str]] | None = None,
    path: Path | str = ".gitignore",
) -> None:
    """Set up the .gitignore for the whole team."""
    entries = get_gitignore_entries(config_files, cache_files)
    if not os.path.isfile(path):
        warn(f" 🔧 We created '{path}' please commit it. 🔧")
        return write_config_file_to_add(entries, "", path=path)
    config_files_to_add = set()
    with open(path, encoding="utf8") as git_ignore:
        gitignore_content = git_ignore.read().split("\n")
    for entry in entries:
        if entry not in gitignore_content:
            if verbose:
                info(f"{entry} is not in the .gitignore")
            config_files_to_add.add(entry)
    return write_config_file_to_add(
        config_files_to_add, "\n".join(gitignore_content), path=path
    )


def get_updated_gitignore_content(
    gitignore_content: str, config_files_to_add: set[str], gitignore_info_text: str
) -> tuple[str, str]:
    text = ""
    file_to_add = "{}\n".format("\n".join(sorted(config_files_to_add)))
    if gitignore_info_text in gitignore_content:
        mode = "w"
        gitignore = gitignore_content.split(f"{gitignore_info_text}\n")
        join = "".join(gitignore[1:])
        text = f"{gitignore[0]}\n{gitignore_info_text}\n{file_to_add}{join}"
    else:
        mode = "a"
        if gitignore_content:
            text += "\n"
        text += f"{gitignore_info_text}\n{file_to_add}"
    return text, mode


def write_config_file_to_add(
    config_files_to_add: Iterable[str], gitignore_content: str, path: Path | str
) -> None:
    if not config_files_to_add:
        return
    config = confuse.Configuration(APPLICATION_NAME, __name__)
    gitignore_info_text = config["gitignore_info_text"].get(str)
    text, mode = get_updated_gitignore_content(
        gitignore_content, set(config_files_to_add), gitignore_info_text
    )
    with open(path, mode, encoding="utf8") as gitignore:
        gitignore.write(text)
    success(f"✨ Updated {path} successfully with {config_files_to_add}. ✨")
