import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Filters, run_async

from ..utils.conf import MEMKEY, settings, set_admin
from ..utils.deco import private_only, send_typing_action

log = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(command='start', filters=Filters.regex(MEMKEY), callback=admin_start))
    dispatcher.add_handler(CommandHandler(command='start', filters=~Filters.regex(MEMKEY), callback=user_start))


@run_async
@private_only
@send_typing_action
def user_start(update: Update, _context: CallbackContext):
    if update.effective_user.id == settings.ADMIN:
        log.info('Admin send /start')
        update.message.reply_text('Hello admin!')
    else:
        log.info('User send /start')
        update.message.reply_text('Hello user!')


@run_async
@private_only
@send_typing_action
def admin_start(update: Update, _context: CallbackContext):
    set_admin(update.effective_user.id)
    log.info(f'{update.effective_user.username} is now admin!')
    update.message.reply_text('You are now admin of this bot!')
