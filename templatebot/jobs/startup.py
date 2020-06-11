import logging

from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, JobQueue, run_async

from ..utils.conf import settings

log = logging.getLogger(__name__)


def init(job_queue: JobQueue):
    job_queue.run_once(callback=startup, when=1)


@run_async
def startup(context: CallbackContext):
    if settings.ADMIN != 0:
        try:
            context.bot.send_message(settings.ADMIN, 'Startup successful!')
        except Unauthorized:
            log.error('Admin, please start the bot so I can send you messages')
        except BadRequest:
            log.error('Invalid ADMIN (telegram id), please check settings.ini')
