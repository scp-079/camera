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
from subprocess import run

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import glovar
from ..functions.etc import code, thread
from ..functions.file import get_downloaded_path
from ..functions.filters import admin_user
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.incoming & filters.private & filters.voice
                   & admin_user)
def speak(client: Client, message: Message) -> bool:
    # Play user's voice
    result = False

    glovar.locks["speak"].acquire()

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id
        file_id = message.voice.file_id

        # Download the voice
        file = get_downloaded_path(client, file_id)

        if not file:
            return True

        # Convert to wav
        run(f"ffmpeg -i {file} {file}.wav", shell=True)

        # Play the audio
        run(f"aplay {file}.wav", shell=True)

        # Delete files
        run(f"rm -f {file} {file}.wav", shell=True)

        # Send the report message
        text = f"{code('Done!')}\n"
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"Speak error: {e}", exc_info=True)
    finally:
        glovar.locks["speak"].release()

    return result
