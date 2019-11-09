import logging
from configparser import RawConfigParser
from threading import Lock
from typing import Dict, List, Set

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""

# [channels]
report_channel_id: int = 0

# [custom]
creator_id: int = 0
video_extension: str = ""
video_path: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    # [channels]
    report_channel_id = int(config["channels"].get("report_channel_id", report_channel_id))
    # [custom]
    creator_id = int(config["custom"].get("creator_id", creator_id))
    video_extension = config["custom"].get("video_extension", video_extension)
    video_path = config["custom"].get("video_path", video_path)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or report_channel_id == 0
        or creator_id == 0
        or video_extension in {"", "[DATA EXPUNGED]"}
        or video_path in {"", "[DATA EXPUNGED]"}):
    raise SystemExit("No proper settings")

# Init

admin_ids: Set[int] = {creator_id}

all_commands: List[str] = ["ping"]

locks: Dict[str, Lock] = {
    "upload": Lock()
}

version: str = "0.0.1"

# Start program
copyright_text = f"Camera v{version}, Copyright (C) 2019 Xiao\n"
print(copyright_text)
