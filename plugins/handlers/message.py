import logging
from subprocess import run

from pyrogram import Client, Filters, Message

from .. import glovar
from ..functions.etc import code, thread
from ..functions.file import get_downloaded_path
from ..functions.filters import admin_user
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.private & Filters.voice
                   & admin_user)
def speak(client: Client, message: Message) -> bool:
    # Play user's voice
    glovar.locks["speak"].acquire()
    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id
        file_id = message.voice.file_id
        file_ref = message.voice.file_ref

        # Download the voice
        file = get_downloaded_path(client, file_id, file_ref)

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

        return True
    except Exception as e:
        logger.warning(f"Speak error: {e}", exc_info=True)
    finally:
        glovar.locks["speak"].release()

    return False
