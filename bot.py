import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import config
from datetime import time
from zoneinfo import ZoneInfo
from handlers.callbacks import register_handlers
from handlers.daily_report import send_daily_report

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='logs/bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        '👋 سلام! بات گزارش روزانه آماده است.'
    )


def main() -> None:
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    register_handlers(app)

    hours, minutes = map(int, config.DAILY_SCHEDULE_TIME.split(':'))
    schedule_time = time(hour=hours, minute=minutes,
                         tzinfo=ZoneInfo(config.TIMEZONE))
    app.job_queue.run_daily(
        send_daily_report,
        time=schedule_time,
        # days=(0,1,2,3,4),
        name='daily-report'
    )

    logger.info('Bot started')
    app.run_polling()


if __name__ == '__main__':
    main()
