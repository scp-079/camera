import logging
from glob import glob
from subprocess import run

from pyrogram import Client

from .. import glovar
from .telegram import send_video

# Enable logging
logger = logging.getLogger(__name__)


def interval_min_01(client: Client) -> bool:
    # Execute every minute
    glovar.locks["upload"].acquire()
    try:
        # Get the file list
        file_list = glob(f"{glovar.video_path}/*.{glovar.video_extension}")

        # Upload and delete
        for file in file_list:
            result = send_video(
                client=client,
                cid=glovar.report_channel_id,
                video=file
            )
            if result:
                run(["sudo", "rm", "-f", file])

        return True
    except Exception as e:
        logger.warning(f"Interval min 01 error: {e}", exc_info=True)
    finally:
        glovar.locks["upload"].release()

    return False
