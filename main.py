#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client

from plugins import glovar
from plugins.functions.timers import interval_min_01

# Enable logging
logger = logging.getLogger(__name__)

# Start
app = Client(
    session_name="bot",
    bot_token=glovar.bot_token
)
app.start()

# Timer
scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
scheduler.add_job(interval_min_01, "interval", [app], minutes=1)
scheduler.start()

# Hold
app.idle()

# Stop
app.stop()
