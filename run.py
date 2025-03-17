import asyncio
import logging
import os
import dotenv
dotenv.load_dotenv()

from aiogram import Dispatcher, Bot, F
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv('ORDER_BOT_TOKEN'))
dp = Dispatcher()
rt = Router()
dp.include_router(rt)

async def getUser(tg_id):
    """Check, if information about user with id = tg_id exists.
    @Returns bool - if user exists"""
    return False
    pass

async def registrateUser(user_info):
    """Create new user with 'user_info' credentials
    @Returns bool - registration end state"""
    # Implement the registration logic here
    # Example:
    logger.info(f"Registering user with info: {user_info}")  # Placeholder action
    return True  # Assuming registration is successful

@rt.message(CommandStart())
async def cmd_start(message: Message):
    """Handle '/start' command """
    if (str(message.from_user.id) != os.getenv("BARISTA_ID")):
        if not (await getUser(str(message.from_user.id))):  # Pass user ID to getUser function. Also corrected the boolean check.
            user_info = {"user_id": message.from_user.id, "username": message.from_user.username, "first_name": message.from_user.first_name, "last_name": message.from_user.last_name}  # Create a dictionary for user info
            await registrateUser(user_info=user_info) # Pass user_info to registration function
            await message.answer("Привет! Это бот твоей любимой кофейни! Нажми на кнопку снизу, чтобы заказать кофе!")
            await message.answer(message.from_user.id)
        else:
            await message.answer("С возвращением! Рады видеть вас снова!")
    else:
        await message.answer("Привет! Готов варить вкусный кофе?")
@rt.message()
async def send_order(message: Message):
    """Handle '/start' command """
    if (message.text == "1"):
        await bot.send_message(chat_id=os.getenv('bots_chat_id'), text="Новый заказ! Пожри кала ")

async def main():
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Bot stopped")

if __name__ == '__main__': # Corrected the if statement.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually")