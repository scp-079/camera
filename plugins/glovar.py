# Camera - Motion detecting camera with Telegram benefits
# Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>
#
# This file is part of Camera.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pickle
from configparser import RawConfigParser
from os.path import exists
from random import randint
from threading import Lock
from typing import Dict, List, Set, Union

from yaml import safe_load

from .checker import check_all, raise_error
from .version import version_control

# Path variables
CONFIG_PATH = "data/config/config.ini"
CUSTOM_LANG_PATH = "data/config/custom.yml"
LOG_PATH = "data/log"
PICKLE_BACKUP_PATH = "data/pickle/backup"
PICKLE_PATH = "data/pickle"
REPORT_PATH = "data/config/report.txt"
RESTART_PATH = "data/config/restart.txt"
SESSION_DIR_PATH = "data/session"
SESSION_PATH = "data/session/bot.session"
TMP_PATH = "data/tmp"

# Version control
version_control()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename=f"{LOG_PATH}/log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [flag]
broken: bool = True

# [auth]
creator_id: int = 0

# [basic]
bot_token: str = ""
ipv6: Union[bool, str] = "False"
prefix: List[str] = []
prefix_str: str = "/!"
restart: int = 19

# [channels]
report_channel_id: int = 0

# [custom]
format_date: str = "%Y/%m/%d"
height: int = 480
manual_link: str = "https://github.com/scp-079/camera/README_CN.md"
video_extension: str = "mp4"
video_path: str = "/home/pi/motion/tmp"
width: int = 640

# [language]
lang: str = "cmn-Hans"

try:
    not exists(CONFIG_PATH) and raise_error(f"{CONFIG_PATH} does not exists")
    config = RawConfigParser()
    config.read(CONFIG_PATH)

    # [auth]
    creator_id = int(config.get("auth", "creator_id", fallback=str(creator_id)))

    # [basic]
    bot_token = config.get("basic", "bot_token", fallback=bot_token)
    ipv6 = config.get("basic", "ipv6", fallback=ipv6)
    ipv6 = eval(ipv6)
    prefix = [p for p in list(config.get("basic", "prefix", fallback=prefix_str)) if p]
    restart = int(config.get("basic", "restart", fallback=str(restart)))

    # [channels]
    report_channel_id = int(config.get("channels", "report_channel_id", fallback=report_channel_id))

    # [custom]
    format_date = config.get("custom", "format_date", fallback=format_date)
    height = int(config.get("custom", "height", fallback=str(height)))
    manual_link = config.get("custom", "manual_link", fallback=manual_link)
    video_extension = config.get("custom", "video_extension", fallback=video_extension)
    video_path = config.get("custom", "video_path", fallback=video_path)
    width = int(config.get("custom", "width", fallback=str(width)))

    # [language]
    lang = config.get("language", "lang", fallback=lang)

    # [flag]
    broken = False
except Exception as e:
    print(f"[ERROR] Read data from {CONFIG_PATH} error, please check the log file")
    logger.warning(f"Read data from {CONFIG_PATH} error: {e}", exc_info=True)

# Check
check_all(
    {
        "auth": {
            "creator_id": creator_id
        },
        "basic": {
            "bot_token": bot_token,
            "ipv6": ipv6,
            "prefix": prefix,
            "restart": restart
        },
        "channels": {
            "report_channel_id": report_channel_id
        },
        "custom": {
            "format_date": format_date,
            "height": height,
            "manual_link": manual_link,
            "video_extension": video_extension,
            "video_path": video_path,
            "width": width
        },
        "language": {
            "lang": lang
        }
    },
    broken
)

# Language Dictionary
lang_dict: dict = {}
LANG_PATH = CUSTOM_LANG_PATH if exists(CUSTOM_LANG_PATH) else f"languages/{lang}.yml"

try:
    with open(LANG_PATH, "r", encoding="utf-8") as f:
        lang_dict = safe_load(f)
except Exception as e:
    logger.critical(f"Reading language YAML file failed: {e}", exc_info=True)
    raise SystemExit("Reading language YAML file failed")

# Init

admin_ids: Set[int] = {creator_id}

all_commands: List[str] = ["ping"]

locks: Dict[str, Lock] = {
    "file": Lock(),
    "speak": Lock(),
    "upload": Lock()
}

updating: bool = False

version: str = "0.0.6"

# Load data from TXT file
if exists(RESTART_PATH):
    with open(RESTART_PATH, "r", encoding="utf-8") as f:
        restart_text = f.read()
        restart_text = restart_text.strip()
else:
    restart_text = str(randint(4, 14))
    with open(RESTART_PATH, "w", encoding="utf-8") as f:
        f.write(restart_text)

# Init data

current: str = ""
# current = "0.0.1"

token: str = ""
# token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# Load data
file_list: List[str] = ["current", "token"]

for file in file_list:
    try:
        try:
            if exists(f"{PICKLE_PATH}/{file}") or exists(f"{PICKLE_BACKUP_PATH}/{file}"):
                with open(f"{PICKLE_PATH}/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"{PICKLE_PATH}/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"{PICKLE_BACKUP_PATH}/{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = f"Camera v{version}, Copyright (C) 2019-2021 SCP-079\n"
print(copyright_text)
