import logging


from pyrogram import Client, Filters, Message

from ..functions.etc import code, thread
from ..functions.filters import admin_user
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.private & Filters.command(["ping"])
                   & admin_user)
def ping(client: Client, message: Message) -> bool:
    try:
        cid = message.chat.id
        text = f"{code('Pong!')}"
        thread(send_message, (client, cid, text))

        return True
    except Exception as e:
        logger.warning(f"Ping error: {e}", exc_info=True)

    return False
