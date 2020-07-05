import logging
import os

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from scanner import Scanner
from db import Guest_db

API_TOKEN = os.environ['API_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = Guest_db()
scanner = Scanner()
guests = dict()

def on_start():
    global guests
    guests = 

async def scanning(time_interval:int):
    while True:
        global guests
        guests = scanner.get_guests()
        await asyncio.sleep(time_interval)
        print(guests)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Bot!\nPowered by aiogram.")

@dp.message_handler(commands=['scan'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.from_user.id, str(guests))

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    dp.loop.create_task(scanning(5))
    executor.start_polling(dp, skip_updates=True)
    