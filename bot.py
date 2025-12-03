import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Dispatcher,Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from services import database as db


load_dotenv()
TOKEN = os.environ.get('TOKEN')


async def on_startup():
    await db.db_start()


async def main() -> None:
    bot = Bot(TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(handlers.router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)
    asyncio.run(main())