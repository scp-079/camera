# Camera

With this program, you can easily create a bot to send camera videos and photos to a Telegram channel.

## How to use

- Read [the document](README_CN.md) to learn more
- Discuss [group](https://t.me/SCP_079_CHAT)

## Requirements

- OS: Raspberry Pi OS
- Python: 3.7 or higher
- pip: `pip install -r requirements.txt` 

## Files

- data
    - The folder will be generated when program starts
- examples
    - `config.ini` -> `../data/config/config.ini` : Configuration example
- languages
    - `cmn-Hans.yml` : Mandarin Chinese (Simplified)
- plugins
    - functions
        - `command.py` : Functions about command
        - `decorators.py` : Some decorators
        - `etc.py` : Miscellaneous
        - `file.py` : Save files
        - `filters.py` : Some filters
        - `program.py` : Functions about program
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
    - handlers
        - `command.py` : Handle commands
        - `message.py`: Handle messages
    - `__init__.py`
    - `checker.py` : Check the format of `config.ini`
    - `glovar.py` : Global variables
    - `start.py` : Execute before client start
    - `version.py` : Execute before main script start
- `.gitignore` : Specifies intentionally untracked files that Git should ignore
- `dictionary.dic` : Project's dictionary
- `LICENSE` : GPLv3
- `main.py` : Start here
- `pip.sh` : Script for updating dependencies
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribution

Contributions are always welcome, whether it's modifying source code to add new features or bug fixes, documenting new file formats or simply editing some grammar.

You can also join the [discuss group](https://t.me/SCP_079_CHAT) if you are unsure of anything.

## Translation

- [Choose Language Tags](https://www.w3.org/International/questions/qa-choosing-language-tags)
- [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)

## Copyright & License

- Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>
- Licensed under the terms of the [GNU General Public License v3](LICENSE).
