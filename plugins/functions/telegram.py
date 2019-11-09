import logging
from typing import Optional, Union

from pyrogram import Client
from pyrogram import InlineKeyboardMarkup, Message
from pyrogram.errors import ButtonDataInvalid, ChannelInvalid, ChannelPrivate, FloodWait, PeerIdInvalid

from .etc import wait_flood

# Enable logging
logger = logging.getLogger(__name__)


def download_media(client: Client, file_id: str, file_ref: str, file_path: str):
    # Download a media file
    result = None
    try:
        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.download_media(message=file_id, file_ref=file_ref, file_name=file_path)
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
    except Exception as e:
        logger.warning(f"Download media {file_id} to {file_path} error: {e}", exc_info=True)

    return result


def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: InlineKeyboardMarkup = None) -> Optional[Union[bool, Message]]:
    # Send a message to a chat
    result = None
    try:
        if not text.strip():
            return None

        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.send_message(
                    chat_id=cid,
                    text=text,
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_to_message_id=mid,
                    reply_markup=markup
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except (PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
            except ButtonDataInvalid:
                logger.warning(f"Send message to {cid} - invalid markup: {markup}")
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result


def send_photo(client: Client, cid: int, photo: str, file_ref: str = None, caption: str = "", mid: int = None,
               markup: InlineKeyboardMarkup = None) -> Optional[Union[bool, Message]]:
    # Send a photo to a chat
    result = None
    try:
        if not photo.strip():
            return None

        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.send_photo(
                    chat_id=cid,
                    photo=photo,
                    file_ref=file_ref,
                    caption=caption,
                    parse_mode="html",
                    reply_to_message_id=mid,
                    reply_markup=markup
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except (PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
            except ButtonDataInvalid:
                logger.warning(f"Send photo {photo} to {cid} - invalid markup: {markup}")
    except Exception as e:
        logger.warning(f"Send photo {photo} to {cid} error: {e}", exc_info=True)

    return result


def send_video(client: Client, cid: int, video: str, file_ref: str = None, caption: str = "", mid: int = None,
               markup: InlineKeyboardMarkup = None) -> Optional[Union[bool, Message]]:
    # Send a video to a chat
    result = None
    try:
        if not video.strip():
            return None

        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.send_video(
                    chat_id=cid,
                    video=video,
                    file_ref=file_ref,
                    caption=caption,
                    parse_mode="html",
                    reply_to_message_id=mid,
                    reply_markup=markup
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except (PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
            except ButtonDataInvalid:
                logger.warning(f"Send video {video} to {cid} - invalid markup: {markup}")
    except Exception as e:
        logger.warning(f"Send video {video} to {cid} error: {e}", exc_info=True)

    return result
