import os

from centralized_pre_commit_conf.prints import info, success, warn


def update_gitignore(args, config_files):
    """Set up the .gitignore for the whole team."""
    if os.path.isfile(".gitignore"):
        config_files_to_add = set()
        with open(".gitignore", encoding="utf8") as gitignore:
            gitignore_content = gitignore.read().split("\n")
            for config_file in config_files:
                if config_file not in gitignore_content:
                    message = "{} is not in the .gitignore".format(config_file)
                    if args.verbose:
                        info(message)
                    config_files_to_add.add(config_file)
    else:
        warn(" 🔧 We created the '.gitignore' please commit it. 🔧")
        config_files_to_add = set(config_files)
    if config_files_to_add:
        with open(".gitignore", "a", encoding="utf8") as gitignore:
            text = "\n# Configuration file added automatically by 'centralized-pre-commit-conf'"
            text += "\n{}\n".format("\n".join(config_files_to_add))
            gitignore.write(text)
    if config_files_to_add:
        success(f" ✨ Updated .gitignore successfully with {config_files_to_add}. ✨")
