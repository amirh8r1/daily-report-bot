from telegram import Update, ForceReply
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
import config

pending_prompt: dict[int, tuple[int, str]] = {}


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data

    if data == 'didn_t_work_but_know':
        prompt_text = f"@{user.username} لطفاً با ریپلای به همین پیغام بنویس که فردا چه کاری قراره انجام بدی؟"
        thread_id = config.FORUM_THREAD_ID or None
        msg = await context.bot.send_message(
            chat_id=config.FORUM_CHAT_ID,
            message_thread_id=thread_id,
            text=prompt_text,
            reply_to_message_id=query.message.message_id,
            reply_markup=ForceReply(selective=True)
        )
        pending_prompt[user.id] = (msg.message_id, data)

    elif data == 'didn_t_work_and_dont_know':
        thread_id = config.FORUM_THREAD_ID or None
        await context.bot.send_message(
            chat_id=config.FORUM_CHAT_ID,
            message_thread_id=thread_id,
            text=f"@{user.username} امروز کاری نکرده و نمی‌دونه فردا باید چی‌کار کنه.\n****\nنیاز به راهنمایی داره!!!"
        )

    elif data == 'manual_report':
        template = (
            "لطفاً با ریپلای به همین پیغام گزارش خود را در قالب زیر بنویسید:\n\n"
            "1. امروز چه کارهایی انجام دادید؟\n"
            "2. چقدر زمان گذاشتید؟\n"
            "3. فردا چه برنامه‌ای دارید؟\n"
            "4. توضیحات تکمیلی (اختیاری)"
        )
        thread_id = config.FORUM_THREAD_ID or None
        msg = await context.bot.send_message(
            chat_id=config.FORUM_CHAT_ID,
            message_thread_id=thread_id,
            text=template,
            reply_to_message_id=query.message.message_id,
            reply_markup=ForceReply(selective=True)
        )
        pending_prompt[user.id] = (msg.message_id, data)


async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    info = pending_prompt.pop(user.id, None)
    if not info:
        return
    prompt_id, prompt_type = info
    text = update.message.text
    chat_id = config.FORUM_CHAT_ID
    thread_id = config.FORUM_THREAD_ID or None

    for msg_id in (prompt_id, update.message.message_id):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass

    if prompt_type == 'didn_t_work_but_know':
        summary = f"@{user.username} امروز کاری نکرده ولی برنامه‌ی فردا:\n\n {text}"
    elif prompt_type == 'manual_report':
        summary = f"@{user.username} گزارش روزانه شما:\n\n{text}"
    else:
        summary = text

    await context.bot.send_message(
        chat_id=chat_id,
        message_thread_id=thread_id,
        text=summary
    )


def register_handlers(app):
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(
            filters.TEXT
            & filters.REPLY
            & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP),
            reply_handler
        )
    )
