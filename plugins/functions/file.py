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
from os import remove
from os.path import exists
from shutil import copyfile
from time import sleep

from pyrogram import Client

from .. import glovar
from .decorators import threaded
from .etc import random_str
from .telegram import download_media

# Enable logging
logger = logging.getLogger(__name__)


def delete_file(path: str) -> bool:
    # Delete a file
    result = False

    try:
        if not(path and exists(path)):
            return False

        result = remove(path) or True
    except Exception as e:
        logger.warning(f"Delete file error: {e}", exc_info=True)

    return result


def get_downloaded_path(client: Client, file_id: str) -> str:
    # Download file, get it's path on local machine
    result = ""

    try:
        if not file_id:
            return ""

        file_path = get_new_path()
        result = download_media(client, file_id, file_path)
    except Exception as e:
        logger.warning(f"Get downloaded path error: {e}", exc_info=True)

    return result


def get_new_path(extension: str = "", prefix: str = "") -> str:
    # Get a new path in tmp directory
    result = ""

    try:
        file_path = random_str(8)

        while exists(f"{glovar.TMP_PATH}/{prefix}{file_path}{extension}"):
            file_path = random_str(8)

        result = f"{glovar.TMP_PATH}/{prefix}{file_path}{extension}"
    except Exception as e:
        logger.warning(f"Get new path error: {e}", exc_info=True)

    return result


@threaded(daemon=False)
def save(file: str) -> bool:
    # Save a global variable to a file
    result = False

    glovar.locks["file"].acquire()

    try:
        if not glovar:
            return False

        with open(f"{glovar.PICKLE_BACKUP_PATH}/{file}", "wb") as f:
            pickle.dump(eval(f"glovar.{file}"), f)

        result = copyfile(f"{glovar.PICKLE_BACKUP_PATH}/{file}", f"{glovar.PICKLE_PATH}/{file}")
    except RuntimeError:
        glovar.locks["file"].release()
        sleep(1)
        return save(file)
    except Exception as e:
        logger.warning(f"Save {file} error: {e}", exc_info=True)
    finally:
        glovar.locks["file"].release()

    return result
