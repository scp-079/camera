import logging
from os import remove
from os.path import exists

from pyrogram import Client

from .etc import random_str
from .telegram import download_media

# Enable logging
logger = logging.getLogger(__name__)


def delete_file(path: str) -> bool:
    # Delete a file
    try:
        if path and exists(path):
            remove(path)

        return True
    except Exception as e:
        logger.warning(f"Delete file error: {e}", exc_info=True)

    return False


def get_downloaded_path(client: Client, file_id: str, file_ref: str) -> str:
    # Download file, get it's path on local machine
    final_path = ""
    try:
        if not file_id:
            return ""

        file_path = get_new_path()
        final_path = download_media(client, file_id, file_ref, file_path)
    except Exception as e:
        logger.warning(f"Get downloaded path error: {e}", exc_info=True)

    return final_path


def get_new_path(extension: str = "") -> str:
    # Get a new path in tmp directory
    result = ""
    try:
        file_path = random_str(8)

        while exists(f"tmp/{file_path}{extension}"):
            file_path = random_str(8)

        result = f"tmp/{file_path}{extension}"
    except Exception as e:
        logger.warning(f"Get new path error: {e}", exc_info=True)

    return result
