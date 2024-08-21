import os
import requests
import logging

from diff_parser import Diff


logging.basicConfig(filename="./updater.log", level=logging.INFO)


class Updater:
    def __init__(self, data: str) -> None:
        print(__file__)
        logging.info("Checking for Updates.")
        repo, version = data.splitlines()

        GITHUB_REPO_URL=f"https://github.com/{repo.strip()}" 
        VERSION=version.strip()
        LATEST_RELEASES_URL=f"{GITHUB_REPO_URL}/releases/latest"
        LATEST_VERSION = requests.head(LATEST_RELEASES_URL).headers['location'].split("/")[-1]
        DIFF_URL=f"{GITHUB_REPO_URL}/compare/{VERSION}...{LATEST_VERSION}.diff"
        RAW_GITHUB_URL=f"https://raw.githubusercontent.com/{repo.strip()}"
        
        UPTODATE = VERSION == LATEST_VERSION

        if UPTODATE:
            logging.info("No updates found.")
            return
        
        # comapring diffs
        resp = requests.get(DIFF_URL)
        diff = Diff(resp.content.decode())


        # downloading and installing updates
        for d in diff:
            if d.type != 'deleted':
                print(f"WRITING: .{d.new_filepath}")
                with open(f'.{d.old_filepath}', 'wb') as file:
                    resp = requests.get(f"{RAW_GITHUB_URL}/{LATEST_VERSION}{d.new_filepath}")
                    file.write(resp.content)
                if d.old_filepath != d.new_filepath:
                    os.rename(d.old_filepath, d.new_filepath)
            elif os.path.exists(f".{d.old_filepath}"):
                print(f"DELETING: .{d.old_filepath}")
                os.remove(f".{d.old_filepath}")

    def setup_auto_run():
        # to be implemented
        pass
