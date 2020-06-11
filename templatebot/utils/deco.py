from functools import wraps

from telegram import Chat, ChatAction, Update
from telegram.ext import CallbackContext

from ..utils.conf import settings


def admin_only(func):
    @wraps(func)
    def restricted_func(update: Update, context: CallbackContext, **kwargs):
        user = update.effective_user.id
        if user == settings.ADMIN:
            return func(update, context, **kwargs)

    return restricted_func


def private_only(func):
    @wraps(func)
    def restricted_func(update: Update, context: CallbackContext, **kwargs):
        chat_type = update.effective_chat.type
        if chat_type == Chat.PRIVATE:
            return func(update, context, **kwargs)

    return restricted_func


def group_only(func):
    @wraps(func)
    def restricted_func(update: Update, context: CallbackContext, **kwargs):
        chat_type = update.effective_chat.type
        if chat_type == Chat.GROUP or chat_type == Chat.SUPERGROUP:
            return func(update, context, **kwargs)

    return restricted_func


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update: Update, context: CallbackContext, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return func(update, context, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_recording_action = send_action(ChatAction.RECORD_AUDIO)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
