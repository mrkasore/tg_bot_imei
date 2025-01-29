import asyncio
from aiogram import Dispatcher
# import logging

from app.handlers import router
from app import orm as db
from app.bot import bot
from app.middleware import WhitelistMiddleware

dp = Dispatcher()
dp.update.middleware(WhitelistMiddleware())

async def on_startup():
    await db.db_start()

async def main():
    # logging.basicConfig(level=logging.INFO)
    await on_startup()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())