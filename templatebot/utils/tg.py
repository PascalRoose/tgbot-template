import logging
import os
import sys
from importlib import import_module

from telegram.bot import Bot
from telegram.error import InvalidToken
from telegram.ext import PicklePersistence, Updater, messagequeue as mq

from ..utils.conf import NAME

log = logging.getLogger(__name__)


class MQBot(Bot):
    # A subclass of Bot which delegates send method handling to MQ
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except Exception as e:
            log.error(e)

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        # Wrapped method would accept new `queued` and `isgroup` OPTIONAL arguments
        return super(MQBot, self).send_message(*args, **kwargs)


def get_updater(bot, persistence_path, use_context=True,
                base_url=None, workers=4, private_key=None,
                private_key_password=None, user_sig_handler=None,
                request_kwargs=None):
    try:
        persistence = PicklePersistence(filename=persistence_path)
        updater = Updater(bot=bot, persistence=persistence, use_context=use_context,
                          base_url=base_url, workers=workers, private_key=private_key,
                          private_key_password=private_key_password, user_sig_handler=user_sig_handler,
                          request_kwargs=request_kwargs)
        return updater
    except InvalidToken:
        log.error('Invalid TOKEN. Please check configurations/settings.py')
        sys.exit(1)


def load_handlers(dispatcher):
    """Load handlers from files in a 'handlers' directory."""
    log.debug('Loading handlers')

    base_path = os.path.join(os.path.dirname(__file__), '../handlers')
    files = os.listdir(base_path)

    # Make sure not to include __pycache__
    try:
        files.remove('__pycache__')
    # Raised when __pycache__ does not exist
    except ValueError:
        pass

    for file_name in files:
        handler_module = os.path.splitext(file_name)[0]

        module = import_module(f'.{handler_module}', f'{NAME}.handlers')
        module.init(dispatcher)


def load_jobs(job_queue):
    """Load jobs from the files in the 'jobs' directory"""
    log.debug('Loading jobs')

    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../jobs')
    files = os.listdir(base_path)

    # Make sure not to include __pycache__
    try:
        files.remove('__pycache__')
    # Raised when __pycache__ does not exist
    except ValueError:
        pass

    for file_name in files:
        job_module = os.path.splitext(file_name)[0]

        module = import_module(f'.{job_module}', f'{NAME}.jobs')
        module.init(job_queue)
