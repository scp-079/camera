# Camera

This bot is used to send camera videos.

## To Do List

- [x] Basic functions

## Requirements

- Python 3.6 or higher.
- pip: `pip install -r requirements.txt` or `pip install -U APScheduler pyrogram[fast]`

## Files

- plugins
    - functions
        - `channel.py` : Send messages to channel
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `group.py` : Functions about group
        - `ids.py` : Modify id lists
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
    - handlers
        - `command.py` : Handle commands
        - `message.py`: Handle messages
    - `glovar.py` : Global variables
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configuration
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip
