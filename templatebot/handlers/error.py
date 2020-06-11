import logging

from telegram import Update
from telegram.error import (BadRequest, ChatMigrated, Conflict, InvalidToken, NetworkError, RetryAfter, TelegramError,
                            TimedOut, Unauthorized)
from telegram.ext import CallbackContext, Dispatcher, run_async

from ..utils.conf import settings

log = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_error_handler(error_handler)


@run_async
def error_handler(update: Update, context: CallbackContext):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        pass
    except BadRequest:
        # handle malformed requests - read more below!
        pass
    except TimedOut:
        # handle slow connection problems
        pass
    except NetworkError:
        # handle other connection problems
        pass
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        pass
    except (Conflict, InvalidToken, RetryAfter, TelegramError):
        # handle all other telegram related errors
        pass
    finally:
        error_msg = (f'An errror has occured\n\n'
                     f'Error: \n{repr(context.error)}\n{str(context.error)}\n\n')

        if update.effective_message.text.startswith('An errror has occured'):
            log.error(error_msg)
            log.error(f'Failed to send previous error message to admin')
            return

        if update is not None:
            message = update.effective_message
            user = update.effective_user
            chat = update.effective_chat

            error_msg = (f'An errror has occured\n\n'
                         f'User: {user.username}\n\n'
                         f'Text:\n{message.text}\n\n'
                         f'Chat:\n'
                         f'- ID: {chat.id}\n'
                         f'- Type: {chat.type}\n'
                         f'- Name: {chat.title if chat.title is not None else user.full_name}\n\n'
                         f'Error: \n{repr(context.error)}\n{str(context.error)}\n\n')

        context.bot.send_message(settings.ADMIN, error_msg)
