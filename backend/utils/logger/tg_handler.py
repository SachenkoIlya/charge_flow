
from dotenv import load_dotenv
import requests
import logging
import os
import aiohttp
load_dotenv()


class TelegramHandler(logging.Handler):

    def __init__(self, token=None, chat_id=None, level=logging.INFO):
        super().__init__(level)
        self.token = token or os.getenv('TG_TOKEN')
        self.chat_id = chat_id or os.getenv('MY_TG_CHAT_ID')

    def emit(self, record):
        log_entry = self.format(record)

        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                data={"chat_id": self.chat_id, "text": log_entry[:4096]}
            )
        except Exception as e:
            print(f"❌ Ошибка отправки лога в Telegram: {e}")


async def send_tg_message(text: str, chat_id: int = None, token=None, kb=None):

    default_tg_token = os.getenv('TG_TOKEN')
    default_chat_id = os.getenv('MY_TG_CHAT_ID')

    target_chat_id = chat_id or default_chat_id
    target_tg_token = token or default_tg_token

    if not target_tg_token or not target_chat_id:
        return

    pyaload = {
        'chat_id': target_chat_id,
        'text': text[:4096],
        'parse_mode': 'HTML'
    }
    if kb:
        pyaload['reply_markup'] = {
            'inline_keyboard': kb
        }
    try:
        async with aiohttp.ClientSession() as sess:

            async with sess.post(
                f"https://api.telegram.org/bot{target_tg_token}/sendMessage",
                json=pyaload
            ) as res:
                if res.status != 200:
                    error_text = await res.text()
                    print(f"⚠️ Ошибка Telegram API ({res.status}): {error_text}")
                else:
                    data = await res.json()
                    print(f"✅ Сообщение отправлено: message_id={data['result']['message_id']}")
    
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения в Telegram: {e}")


def send_photo_to_telegram(image_path: str, caption: str = ""):
    """
    Отправка изображения в Telegram-бот.
    Необходимо, чтобы переменные окружения TG_BOT_TOKEN и TG_CHAT_ID были заданы.
    """
    bot_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("MY_TG_CHAT_ID")

    if not bot_token or not chat_id:
        raise ValueError(
            "TG_BOT_TOKEN или TG_CHAT_ID не заданы в переменных окружения.")

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    with open(image_path, 'rb') as photo:
        response = requests.post(url, data={
            'chat_id': chat_id,
            'caption': caption
        }, files={
            'photo': photo
        })

    if response.status_code != 200:
        raise Exception(f"Ошибка отправки фото: {response.text}")
