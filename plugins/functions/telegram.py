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
from typing import Iterable, Optional, Union

from pyrogram import Client
from pyrogram.errors import (ButtonDataInvalid, ButtonUrlInvalid, ChannelInvalid, ChannelPrivate, ChatAdminRequired,
                             FloodWait, MessageDeleteForbidden, PeerIdInvalid, ReplyMarkupInvalid)
from pyrogram.types import InlineKeyboardMarkup, Message, ReplyKeyboardMarkup

from .decorators import retry
from .etc import delay

# Enable logging
logger = logging.getLogger(__name__)


def delete_messages(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)

        if len(mids) <= 100:
            return delete_messages_100(client, cid, mids)

        mids_list = [mids[i:i + 100] for i in range(0, len(mids), 100)]
        result = bool([delete_messages_100(client, cid, mids) for mids in mids_list])
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def delete_messages_100(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)
        result = client.delete_messages(chat_id=cid, message_ids=mids)
    except FloodWait as e:
        logger.warning(f"Delete message in {cid} - Sleep for {e.x} second(s)")
        raise e
    except MessageDeleteForbidden:
        return False
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def download_media(client: Client, file_id: str, file_path: str) -> Optional[str]:
    # Download a media file
    result = None

    try:
        result = client.download_media(message=file_id, file_name=file_path)
    except FloodWait as e:
        logger.warning(f"Download media {file_id} - Sleep for {e.x} second(s)")
        raise e
    except Exception as e:
        logger.warning(f"Download media {file_id} to {file_path} error: {e}", exc_info=True)

    return result


@retry
def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> Union[bool, Message, None]:
    # Send a message to a chat
    result = None

    try:
        if not text.strip():
            return None

        result = client.send_message(
            chat_id=cid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=mid,
            reply_markup=markup
        )
    except FloodWait as e:
        logger.warning(f"Send message to {cid} - Sleep for {e.x} second(s)")
        raise e
    except (ButtonDataInvalid, ButtonUrlInvalid, ReplyMarkupInvalid):
        logger.warning(f"Send message to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result


@retry
def send_photo(client: Client, cid: int, photo: str, caption: str = "", mid: int = None,
               markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> Union[bool, Message, None]:
    # Send a photo to a chat
    result = None

    try:
        if not photo.strip():
            return None

        result = client.send_photo(
            chat_id=cid,
            photo=photo,
            caption=caption,
            parse_mode="html",
            reply_to_message_id=mid,
            reply_markup=markup
        )
    except FloodWait as e:
        logger.warning(f"Send photo {photo} to {cid} - Sleep for {e.x} second(s)")
        raise e
    except (ButtonDataInvalid, ButtonUrlInvalid, ReplyMarkupInvalid):
        logger.warning(f"Send photo {photo} to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Send photo {photo} to {cid} error: {e}", exc_info=True)

    return result


def send_report_message(secs: int, client: Client, cid: int, text: str, mid: int = None,
                        markup: InlineKeyboardMarkup = None) -> Optional[bool]:
    # Send a message that will be auto deleted to a chat
    result = None

    try:
        result = send_message(
            client=client,
            cid=cid,
            text=text,
            mid=mid,
            markup=markup
        )

        if not result:
            return None

        mid = result.message_id
        mids = [mid]
        result = delay(secs, delete_messages, [client, cid, mids])
    except Exception as e:
        logger.warning(f"Send report message to {cid} error: {e}", exc_info=True)

    return result


@retry
def send_video(client: Client, cid: int, video: str, caption: str = "",
               width: int = 0, height: int = 0, mid: int = None,
               markup: InlineKeyboardMarkup = None) -> Union[bool, Message, None]:
    # Send a video to a chat
    result = None

    try:
        if not video.strip():
            return None

        result = client.send_video(
            chat_id=cid,
            video=video,
            caption=caption,
            parse_mode="html",
            width=width,
            height=height,
            reply_to_message_id=mid,
            reply_markup=markup
        )
    except FloodWait as e:
        logger.warning(f"Send video {video} to {cid} - Sleep for {e.x} second(s)")
        raise e
    except (ButtonDataInvalid, ButtonUrlInvalid, ReplyMarkupInvalid):
        logger.warning(f"Send video {video} to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Send video {video} to {cid} error: {e}", exc_info=True)

    return result
