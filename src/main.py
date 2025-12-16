import os
import requests
import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
OWM_TOKEN = os.getenv('OWM_TOKEN')

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.reply("Привет! Напиши город, и я пришлю погоду.")

@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text
    logger.info(f"User {message.from_user.id} requested weather for: {city}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_TOKEN}&units=metric&lang=ru"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            await message.reply(f"В {city} сейчас {temp}°C, {desc}.")
            logger.info(f"Weather sent for {city}: {temp}°C, {desc}")
        else:
            await message.reply("Не нашёл такой город. Попробуй ещё раз!")
            logger.warning(f"City not found: {city}")
    except Exception as e:
        await message.reply("Произошла ошибка при получении погоды.")
        logger.error(f"Error fetching weather for {city}: {e}")

if __name__ == '__main__':
    logger.info("Bot started")
    executor.start_polling(dp)