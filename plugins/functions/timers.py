import logging
from glob import glob
from subprocess import run

from pyrogram import Client

from .. import glovar
from .etc import code
from .telegram import send_video

# Enable logging
logger = logging.getLogger(__name__)


def interval_min_01(client: Client) -> bool:
    # Execute every minute
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
            text = (f"日期：{code(f'{year} 年 {month} 月 {day} 日')}\n"
                    f"时间：{code(f'{hour} 点 {minute} 分 {second} 秒')}\n")

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

        return True
    except Exception as e:
        logger.warning(f"Interval min 01 error: {e}", exc_info=True)
    finally:
        glovar.locks["upload"].release()

    return False
