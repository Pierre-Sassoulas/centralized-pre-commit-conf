import os
import warnings
from pathlib import Path
from typing import Dict

import confuse
import requests
from urllib3.exceptions import InsecureRequestWarning

from centralized_pre_commit_conf.parse_args import get_url_from_args
from centralized_pre_commit_conf.prints import error, info, success, warn


class Result:
    # pylint: disable=too-few-public-methods

    downloaded: bool
    new_content: bool
    replaced: bool
    failed_download: requests.Response

    def __init__(self):
        self.downloaded = False
        self.new_content = False
        self.replaced = False
        self.failed_download = None

    def __repr__(self):
        return f"{self.downloaded} {self.replaced} {self.new_content}"


def download_configuration(config: confuse.Configuration) -> None:
    results = {}
    config_files = config["configuration_files"].get(list)
    url = get_url_from_args(config["repository"].get(str), config["branch"].get(str), config["path"].get(str))
    insecure = config["insecure"].get(bool)
    verbose = config["verbose"].get(bool)
    for config_file in config_files:
        result = Result()
        config_file_url = f"{url}/{config_file}"
        if verbose:
            info(f"Downloading '{config_file}' from '{config_file_url}'")
        request_result = recover_new_content(config_file_url, insecure)
        result.downloaded = request_result.status_code == 200
        if not result.downloaded:
            result.failed_download = request_result
            results[config_file] = result
            continue
        path = Path(config_file_url)
        old_content = None
        file_already_exists = os.path.exists(config_file)
        if file_already_exists:
            old_content = read_current_file(path)
        result.new_content = old_content != request_result.content
        if not file_already_exists or (result.new_content and config["replace_existing"].get(bool)):
            result.replaced = True
            write_new_content(path, request_result)
        results[config_file] = result
    display_results(results)


def display_results(results: Dict[str, Result]) -> None:
    max_len: int = max(len(c) for c in results)
    failed: int = 0
    no_new_content: int = 0
    not_replaced: int = 0
    replaced: int = 0
    for file, result in results.items():
        formatted_config: str = "{:{align}{width}}".format(file, align="<", width=max_len)
        if not result.downloaded:
            failed += 1
            details = f"{result.failed_download.url} HTTP{result.failed_download.status_code}"
            error(f"{formatted_config} : 🎻 Download failed 🎻 : {details}")
        elif not result.new_content:
            no_new_content += 1
            success(f"{formatted_config} : ✨ Already up to date ✨")
        elif result.replaced:
            replaced += 1
            success(f"{formatted_config} : 🎉✨ Updated with new content ✨🎉")
        else:
            not_replaced += 1
            warn(f"{formatted_config} : 🔔 already exists 🔔")
    if not results:
        warn("Nothing to recover ❓")
        return
    if failed != 0:
        plural = "s were" if failed != 1 else " was"
        error(f"🎻 {failed} configuration file{plural} not recovered correctly. 🎻")
    if no_new_content != 0:
        plural = "s" if no_new_content > 1 else ""
        success(f"✨ {no_new_content} configuration file{plural} already up to date ✨")
    if not_replaced != 0:
        plural = "s" if not_replaced > 1 else ""
        warn(f"🔔 {not_replaced} file{plural} not replaced. Use '-f' or '--replace-existing' to force erase. 🔔")
    if replaced != 0:
        plural = "s" if replaced > 1 else ""
        success(f"🎉✨ {replaced} configuration file{plural} updated. ✨🎉")


def recover_new_content(config_file_url: str, insecure: bool) -> requests.Response:
    with warnings.catch_warnings(record=True) as messages:
        if insecure:
            result = requests.get(config_file_url, verify=False)
        else:
            result = requests.get(config_file_url)
        for msg in messages:
            if not insecure or msg.category is not InsecureRequestWarning:
                warn(msg.message)
    return result


def write_new_content(path: Path, request_result: requests.Response) -> None:
    with open(path.name, "wb") as f:
        f.write(request_result.content)


def check_download(config_file_url: str, request_result: requests.Response) -> bool:
    if request_result.status_code != 200:
        error_msg = f"download failed 💥\nHTTP status {request_result.status_code} !"
        error(f"💥 '{config_file_url}' {error_msg}")
        return False
    return True


def read_current_file(path: Path) -> bytes:
    with open(path.name, "rb") as f:
        old_content = f.read()
    return old_content
