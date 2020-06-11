#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram.ext import messagequeue as mq
from telegram.utils import helpers
from telegram.utils.request import Request

from .utils.conf import settings, DIRS, MEMKEY
from .utils.log import init_logger
from .utils.tg import MQBot, get_updater, load_handlers, load_jobs

mqueue = mq.MessageQueue(all_burst_limit=10, all_time_limit_ms=3000)
request = Request(con_pool_size=8)
bot = MQBot(token=settings.TOKEN, request=request, mqueue=mqueue)

init_logger(os.path.join(DIRS.user_log_dir, f'{bot.get_me().username}.log'))
log = logging.getLogger(__name__)

persistance_path = os.path.join(DIRS.user_cache_dir, 'telegram.pkl')
updater = get_updater(bot=bot, persistence_path=persistance_path)

load_handlers(updater.dispatcher)
load_jobs(updater.job_queue)

if settings.ADMIN == 0:
    print(f'Please start the bot using the following link to become admin: '
          f'{helpers.create_deep_linked_url(bot.get_me().username, MEMKEY, group=False)}')

if settings.WEBHOOK.ENABLED:
    updater.start_webhook(listen=settings.WEBHOOK.IP,
                          port=settings.WEBHOOK.PORT,
                          url_path=settings.WEBHOOK.PATH,
                          webhook_url=settings.WEBHOOK.URL)
    log.info(f'Started webhook listener on: {settings.WEBHOOK.URL}')
else:
    updater.start_polling()
    log.info('Started polling...')

updater.idle()
