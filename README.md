# PyUpdater

`auto-update` is a Python package designed to update Python projects installed on client systems that do not have Git installed. It retrieves the latest release from a specified GitHub repository, compares it with the currently installed version, and updates the project accordingly.


## Installation

You can install PyUpdater via pip:

```bash
pip install auto-update
```

# Usage

Create a new file `_auto_update.py` in the project root. Replace `owner` with your github username and `repo` with your github repository. Replace `release` with your release name.

### _auto_update.py
```python
"""
{owner}/{repo}
{release}
"""

from auto_update import Updater


updater = Updater(__doc__.strip())
```


`Updater` will then check for updates and apply them if necessary. It will log its activities to a file named updater.log in the current directory.

# License
This project is licensed under the MIT [License](https://github.com/shaiksamad/auto-update/blob/main/LICENSE) - see the LICENSE file for details.

