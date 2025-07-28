from celery import shared_task
from telegram import Bot
from django.conf import settings


@shared_task
def send_telegram_message(chat_id: int, text: str):
    """Создание задачи для Telegram."""

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=chat_id, text=text)
