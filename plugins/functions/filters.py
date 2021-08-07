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
from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def is_admin_user(_, __, update: Union[CallbackQuery, Message]) -> bool:
    # Check if the user who sent the message is an admin
    result = False

    try:
        if isinstance(update, CallbackQuery):
            message = update.message
        else:
            message = update

        if not message.from_user:
            return False

        uid = message.from_user.id

        if uid in glovar.admin_ids:
            return True
    except Exception as e:
        logger.warning(f"Is class c error: {e}")

    return result


def is_creator_user(_, __, update: Union[CallbackQuery, Message]) -> bool:
    # Check if the user who sent the message is the creator
    result = False

    try:
        if isinstance(update, CallbackQuery):
            message = update.message
        else:
            message = update

        if not message.from_user:
            return False

        uid = message.from_user.id

        if uid == glovar.creator_id:
            return True
    except Exception as e:
        logger.warning(f"Is creator user error: {e}", exc_info=True)

    return result


admin_user = filters.create(
    func=is_admin_user,
    name="Admin User"
)

creator_user = filters.create(
    func=is_creator_user,
    name="Creator User"
)
