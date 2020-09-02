import os
from pathlib import Path
from typing import Iterable, Set, Tuple, Union

import confuse
from centralized_pre_commit_conf.constants import APPLICATION_NAME
from centralized_pre_commit_conf.prints import info, success, warn


def update_gitignore(config_files: Iterable[str], verbose: bool, path: Union[Path, str] = ".gitignore") -> None:
    """Set up the .gitignore for the whole team."""
    if not os.path.isfile(path):
        warn(f" 🔧 We created '{path}' please commit it. 🔧")
        return write_config_file_to_add(set(config_files), "", path=path)
    config_files_to_add = set()
    with open(path, encoding="utf8") as git_ignore:
        gitignore_content = git_ignore.read().split("\n")
    for config_file in config_files:
        if config_file not in gitignore_content:
            if verbose:
                info("{} is not in the .gitignore".format(config_file))
            config_files_to_add.add(config_file)
    return write_config_file_to_add(config_files_to_add, "\n".join(gitignore_content), path=path)


def get_updated_gitignore_content(
    gitignore_content: str, config_files_to_add: Set[str], gitignore_info_text: str
) -> Tuple[str, str]:
    text = ""
    file_to_add = "{}\n".format("\n".join(sorted(config_files_to_add)))
    if gitignore_info_text in gitignore_content:
        mode = "w"
        gitignore = gitignore_content.split(f"{gitignore_info_text}\n")
        text = f"{gitignore[0]}\n{gitignore_info_text}\n{file_to_add}{''.join(gitignore[1:])}"
    else:
        mode = "a"
        if gitignore_content:
            text += "\n"
        text += f"{gitignore_info_text}\n{file_to_add}"
    return text, mode


def write_config_file_to_add(config_files_to_add: Iterable[str], gitignore_content: str, path: str) -> None:
    if not config_files_to_add:
        return
    config = confuse.Configuration(APPLICATION_NAME, __name__)
    gitignore_info_text = config["gitignore_info_text"].get(str)
    text, mode = get_updated_gitignore_content(gitignore_content, set(config_files_to_add), gitignore_info_text)
    with open(path, mode, encoding="utf8") as gitignore:
        gitignore.write(text)
    success(f"✨ Updated {path} successfully with {config_files_to_add}. ✨")
