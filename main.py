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

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, idle

from plugins import glovar
from plugins.functions.etc import delay, get_int
from plugins.functions.program import restart_program
from plugins.functions.timers import interval_min_01, log_rotation
from plugins.start import init, renew

# Enable logging
logger = logging.getLogger(__name__)

# Init
init()

# Renew session
renew()

# Config session
app = Client(
    session_name="bot",
    ipv6=glovar.ipv6,
    bot_token=glovar.bot_token,
    workdir=glovar.SESSION_DIR_PATH,
    config_file=glovar.CONFIG_PATH,
    sleep_threshold=0
)
app.start()

# Start the bot
delay(10, restart_program, [app, glovar.creator_id])

# Timer
scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
scheduler.add_job(interval_min_01, "interval", [app], minutes=1)
scheduler.add_job(log_rotation, "cron", hour=23, minute=59)
scheduler.add_job(restart_program, "cron", [app], hour=glovar.restart, minute=get_int(glovar.restart_text))
scheduler.start()

# Hold
idle()

# Stop
app.stop()
