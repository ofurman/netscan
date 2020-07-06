import logging
import os

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from scanner import Scanner
from db import Guest_db

API_TOKEN = os.environ['API_TOKEN']
print(API_TOKEN == "1319401421:AAFdcNTzaok070dbthlfd3QYQQR2TGMd8WA")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="1319401421:AAFdcNTzaok070dbthlfd3QYQQR2TGMd8WA")
dp = Dispatcher(bot)
db = Guest_db()
scanner = Scanner()
guests = dict()

def on_start():
    global guests
    guests = db.get_all()

def on_close():
    global guests
    db.set_guests(guests)

async def scanning(time_interval:int):
    while True:
        global guests
        actual_guests = scanner.get_guests()
        new_guests = set(guests.keys()).symmetric_difference(set(actual_guests.keys()))
        if new_guests in set(guests.keys()):
            db.remove_guests(new_guests):
        elif new_guests in set(actual_guests.keys()):
            
        await asyncio.sleep(time_interval)
        logging.info("Scanned")


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Bot!\nPowered by aiogram.")

@dp.message_handler(commands=['scan'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/scan` command
    """
    guests = scanner.get_guests()
    await bot.send_message(message.from_user.id, str(guests))

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    dp.loop.create_task(scanning(5))
    executor.start_polling(dp, skip_updates=True, on_startup=on_start, on_shutdown=on_close)
    