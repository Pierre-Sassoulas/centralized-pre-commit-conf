import os
import warnings
from pathlib import Path

import requests

from centralized_pre_commit_conf.prints import error, info, success, warn
from urllib3.exceptions import InsecureRequestWarning


def download_configuration(config_files, replace_existing, url, verbose, insecure):
    download_fail = 0
    download_success = 0
    for config_file in config_files:
        max_len = max(len(c) for c in config_files)
        if os.path.exists(config_file) and not replace_existing:
            formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
            warn(f"Found existing {formatted_config} ⁉️  Use '-f' or '--replace-existing' to force erase.")
            continue
        if download_configuration_file(f"{url}/{config_file}", config_file, max_len, verbose, insecure):
            download_success += 1
        else:
            download_fail += 1
    if download_fail == 0:
        if download_success > 0:
            plural = "s" if download_success > 1 else ""
            success(f"🎉 {download_success} configuration file{plural} recovered. 🎉")
        else:
            warn("All configuration files already existed.")
    else:
        pluralization = "s were" if download_fail != 1 else " was"
        warn(f"🎻 {download_fail} configuration file{pluralization} not recovered correctly. 🎻")


def download_configuration_file(file_to_download, config_file, max_len, verbose, insecure):
    kwargs = {}
    if insecure:
        kwargs = {"verify": False}
    if verbose:
        info(f"Downloading {config_file} from {file_to_download} with option {kwargs}")
    with warnings.catch_warnings(record=True) as messages:
        result = requests.get(file_to_download, **kwargs)
        for msg in messages:
            if not insecure or msg.category is not InsecureRequestWarning:
                warn(msg.message)
    path = Path(file_to_download)
    with open(path.name, "wb") as f:
        f.write(result.content)
    if result.status_code != 200:
        error_msg = f"download failed 💥\nHTTP status {result.status_code} !"
        if result.status_code == 404:
            error_msg = "not found. Are you sure it exists ? 💥"
        error(f"💥 '{file_to_download}' {error_msg}")
    else:
        formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
        success("✨ Successfully retrieved {} ✨".format(formatted_config))
    return result.status_code == 200
