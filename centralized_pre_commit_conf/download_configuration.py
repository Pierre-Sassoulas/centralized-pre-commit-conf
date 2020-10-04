import os
import warnings
from pathlib import Path

import confuse
import requests
from urllib3.exceptions import InsecureRequestWarning

from centralized_pre_commit_conf.parse_args import get_url_from_args
from centralized_pre_commit_conf.prints import error, info, success, warn


def download_configuration(config: confuse.Configuration) -> None:
    download_fail = 0
    download_success = 0
    config_files = config["configuration_files"].get(list)
    max_len = max(len(c) for c in config_files)
    url = get_url_from_args(config["repository"].get(str), config["branch"].get(str), config["path"].get(str))
    insecure = config["insecure"].get(bool)
    verbose = config["verbose"].get(bool)
    for config_file in config_files:
        if os.path.exists(config_file) and not config["replace_existing"].get(bool):
            formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
            warn(f"Found existing {formatted_config} ⁉️  Use '-f' or '--replace-existing' to force erase.")
            continue
        config_file_url = f"{url}/{config_file}"
        if verbose:
            info(f"Downloading '{config_file}' from '{config_file_url}'")
        result = recover_new_content(config_file_url, insecure)
        path = Path(config_file_url)
        write_new_content(path, result)
        if check_download(config_file, config_file_url, max_len, result):
            download_success += 1
        else:
            download_fail += 1
    display_results(download_fail, download_success)


def display_results(download_fail, download_success):
    if download_fail == 0:
        if download_success > 0:
            plural = "s" if download_success > 1 else ""
            success(f"🎉 {download_success} configuration file{plural} recovered. 🎉")
        else:
            warn("All configuration files already existed.")
    else:
        pluralization = "s were" if download_fail != 1 else " was"
        warn(f"🎻 {download_fail} configuration file{pluralization} not recovered correctly. 🎻")


def recover_new_content(config_file_url, insecure):
    with warnings.catch_warnings(record=True) as messages:
        if insecure:
            result = requests.get(config_file_url, verify=False)
        else:
            result = requests.get(config_file_url)
        for msg in messages:
            if not insecure or msg.category is not InsecureRequestWarning:
                warn(msg.message)
    return result


def write_new_content(path: Path, result):
    with open(path.name, "wb") as f:
        f.write(result.content)


def check_download(config_file, config_file_url, max_len, result):
    if result.status_code != 200:
        error_msg = f"download failed 💥\nHTTP status {result.status_code} !"
        if result.status_code == 404:
            error_msg = "not found. Are you sure it exists ? 💥"
        error(f"💥 '{config_file_url}' {error_msg}")
        return False
    formatted_config = "{:{align}{width}}".format(config_file, align="<", width=max_len)
    success("✨ Successfully retrieved {} ✨".format(formatted_config))
    return True


def read_current_file(path: Path) -> bytes:
    with open(path.name, "wb") as f:
        old_content = f.read()
    return old_content
