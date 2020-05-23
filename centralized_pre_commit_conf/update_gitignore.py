import os

from centralized_pre_commit_conf.configuration import GITIGNORE_INFO_TEXT
from centralized_pre_commit_conf.prints import info, success, warn


def update_gitignore(config_files, verbose, path=".gitignore") -> None:
    """Set up the .gitignore for the whole team."""
    if not os.path.isfile(path):
        warn(f" 🔧 We created '{path}' please commit it. 🔧")
        return write_config_file_to_add(set(config_files), [""], path=path)
    config_files_to_add = set()
    with open(path, encoding="utf8") as git_ignore:
        gitignore_content = git_ignore.read().split("\n")
    for config_file in config_files:
        if config_file not in gitignore_content:
            if verbose:
                info("{} is not in the .gitignore".format(config_file))
            config_files_to_add.add(config_file)
    return write_config_file_to_add(config_files_to_add, "\n".join(gitignore_content), path=path)


def get_updated_gitignore_content(gitignore_content, config_files_to_add):
    text = ""
    file_to_add = "{}\n".format("\n".join(sorted(config_files_to_add)))
    if GITIGNORE_INFO_TEXT in gitignore_content:
        mode = "w"
        gitignore = gitignore_content.split(f"{GITIGNORE_INFO_TEXT}\n")
        text = f"{gitignore[0]}\n{GITIGNORE_INFO_TEXT}\n{file_to_add}{''.join(gitignore[1:])}"
    else:
        mode = "a"
        if gitignore_content:
            text += "\n"
        text += f"{GITIGNORE_INFO_TEXT}\n{file_to_add}"
    return text, mode


def write_config_file_to_add(config_files_to_add: list, gitignore_content: list, path: str) -> None:
    if not config_files_to_add:
        return
    text, mode = get_updated_gitignore_content(gitignore_content, config_files_to_add)
    with open(path, mode, encoding="utf8") as gitignore:
        gitignore.write(text)
    success(f" ✨ Updated {path} successfully with {config_files_to_add}. ✨")
