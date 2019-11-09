import logging

from pyrogram import Filters, Message

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def is_admin_user(_, message: Message) -> bool:
    # Check if the user who sent the message is an admin
    try:
        if not message.from_user:
            return False

        uid = message.from_user.id
        if uid in glovar.admin_ids:
            return True
    except Exception as e:
        logger.warning(f"Is class c error: {e}")

    return False


def is_creator_user(_, message: Message) -> bool:
    # Check if the user who sent the message is the creator
    try:
        if not message.from_user:
            return False

        uid = message.from_user.id
        if uid == glovar.creator_id:
            return True
    except Exception as e:
        logger.warning(f"Is creator user error: {e}", exc_info=True)

    return False


admin_user = Filters.create(
    func=is_admin_user,
    name="Admin User"
)

creator_user = Filters.create(
    func=is_creator_user,
    name="Creator User"
)
