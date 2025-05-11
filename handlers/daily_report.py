from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
import config


async def send_daily_report(application: Application) -> None:
    text = (
        "🔔 گزارش روزانه\n\n"
        "1️⃣ امروز چه کارهایی انجام دادی؟\n"
        "2️⃣ چقدر زمان گذاشتی؟\n"
        "3️⃣ آیا می‌دونی فردا باید چی‌کار کنی؟\n"
        "4️⃣ یک توضیح کوتاه از برنامه فردا\n\n"
        "👇 می‌تونی سریعاً از گزینه‌های زیر استفاده کنی:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🟢 کاری نکردم ولی می‌دونم فردا چی‌کار کنم", callback_data='didn_t_work_but_know')],
        [InlineKeyboardButton("🔴 کاری نکردم و نمی‌دونم فردا چی‌کار کنم",
                              callback_data='didn_t_work_and_dont_know')],
        [InlineKeyboardButton("✍️ گزارش کار امروزم",
                              callback_data='manual_report')]
    ])

    thread_id = config.FORUM_THREAD_ID if config.FORUM_THREAD_ID != 0 else None

    await application.bot.send_message(
        chat_id=config.FORUM_CHAT_ID,
        message_thread_id=thread_id,
        text=text,
        reply_markup=keyboard
    )
