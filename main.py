import os
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from dotenv import load_dotenv

import asyncio

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
OWM_TOKEN = os.getenv("OWM_TOKEN")

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_TOKEN}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"Погода в {city}: {temp}°C, {desc}"
            else:
                return "Город не найден или ошибка API."

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Напиши название города, и я пришлю погоду.")

@dp.message(F.text)
async def weather(message: Message):
    city = message.text.strip()
    result = await get_weather(city)
    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())