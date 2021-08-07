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
from glob import glob
from subprocess import run

from pyrogram import Client

from .. import glovar
from .etc import code, lang, get_readable_time
from .file import move_file
from .telegram import send_video

# Enable logging
logger = logging.getLogger(__name__)


def interval_min_01(client: Client) -> bool:
    # Execute every minute
    result = False

    glovar.locks["upload"].acquire()

    try:
        # Get the file list
        file_list = glob(f"{glovar.video_path}/*.{glovar.video_extension}")
        file_list.sort()

        # Upload and delete
        for file in file_list:
            if not run(f"sudo -u motion lsof -c motion | grep {file}", shell=True).returncode:
                continue

            filename = file.split("/")[-1].split("-")[-1].split(".")[0]

            year = filename[0:4]
            month = filename[4:6]
            day = filename[6:8]
            hour = filename[8:10]
            minute = filename[10:12]
            second = filename[12:14]

            text = f"{lang('date')}{lang('colon')}{code(glovar.format_date)}\n"
            text = text.replace("%Y", year)
            text = text.replace("%m", month)
            text = text.replace("%d", day)
            text += f"{lang('time')}{lang('colon')}{code(f'{hour}:{minute}:{second}')}\n"

            result = send_video(
                client=client,
                cid=glovar.report_channel_id,
                video=file,
                caption=text,
                width=glovar.width,
                height=glovar.height
            )

            if not result:
                continue

            run(f"sudo -u motion rm -f {file}", shell=True)

        result = True
    except Exception as e:
        logger.warning(f"Interval min 01 error: {e}", exc_info=True)
    finally:
        glovar.locks["upload"].release()

    return result


def log_rotation() -> bool:
    # Log rotation
    result = False

    try:
        move_file(f"{glovar.LOG_PATH}/log", f"{glovar.LOG_PATH}/log-{get_readable_time(the_format='%Y%m%d')}")

        with open(f"{glovar.LOG_PATH}/log", "w", encoding="utf-8") as f:
            f.write("")

        # Reconfigure the logger
        [logging.root.removeHandler(handler) for handler in logging.root.handlers[:]]
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.WARNING,
            filename=f"{glovar.LOG_PATH}/log",
            filemode="a"
        )

        run(f"find {glovar.LOG_PATH}/log-* -mtime +30 -delete", shell=True)

        result = True
    except Exception as e:
        logger.warning(f"Log rotation error: {e}", exc_info=True)

    return result
