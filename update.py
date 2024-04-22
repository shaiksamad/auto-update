import requests
from diff_parser import Diff
import logging
import os

from _auto_updater import __doc__

print(__doc__.strip())

logging.basicConfig(filename="./updater.log", level=logging.INFO)

logging.info("Checking for Updates.")

# getting installed relese info
with open('.version') as file:
    repo, version = file.readlines()

GITHUB_REPO_URL=f"https://github.com/{repo.strip()}" 
RAW_GITHUB_URL=f"https://raw.githubusercontent.com/{repo.strip()}"
VERSION=version.strip()


# checking for latest release
url = GITHUB_REPO_URL + "/releases/latest"
LATEST_VERSION = requests.head(url).headers['location'].split("/")[-1]
UPTODATE = VERSION == LATEST_VERSION

if UPTODATE:
    logging.info("No updates found.")
    exit(0)


# comapring versions (getting diffs)
resp = requests.get(f"{GITHUB_REPO_URL}/compare/{VERSION}...{LATEST_VERSION}.diff")
diff = Diff(resp.content.decode())


# downloading and installing updates
for d in diff:
    if d.type != 'deleted':
        print(f"WRITING: .{d.filepath}")
        with open(f'.{d.filepath}', 'wb') as file:
            resp = requests.get(f"{RAW_GITHUB_URL}/{LATEST_VERSION}{d.filepath}")
            file.write(resp.content)
    elif os.path.exists(f".{d.filepath}"):
        print(f"DELETING: .{d.filepath}")
        os.remove(f".{d.filepath}")


print(VERSION, LATEST_VERSION, UPTODATE)

