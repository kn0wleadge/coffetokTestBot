import asyncio
import logging
import datetime
import os
import json
import dotenv
dotenv.load_dotenv()

from aiogram import Dispatcher, Bot, F
from aiogram import Router, types
from aiogram.enums.content_type import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value, HashTag
from aiogram.filters.callback_data import CallbackData
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from database import async_main, async_session, Orders
from sqlalchemy import select, insert, update

class OrderCallbackData(CallbackData, prefix = 'Order'):
                state: bool
                tg_id: int
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv('ORDER_BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
rt = Router()


dp.include_router(rt)
@rt.message(F.content_type == ContentType.WEB_APP_DATA)
async def parse_data(message: types.Message):
    """Handle order data, create"""
    #data = json.loads(message.web_app_data.data)
    data = message.web_app_data.data
    async with async_session() as session:
         logging.info(data)
         await session.execute(insert(Orders).values(odata=json.loads(data),
                                                     isaccepted=0, iscooking=0, 
                                                     isready=0, ispayed = 0))
         await session.commit()
    await message.reply("Ваш заказ создан. Ожидайте подтверждения!")
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
    # Checking, if user is Barista
    if (str(message.from_user.id) != os.getenv("BARISTA_ID")):
        # Checking if user already used this application
        if not (await getUser(str(message.from_user.id))): 
            #await registrateUser(user_info=user_info) 
            webAppInfo = types.WebAppInfo(url = "https://resplendent-genie-747a6e.netlify.app")
            builder = ReplyKeyboardBuilder()
            builder.add(types.KeyboardButton(text='Заказать кофе', web_app=webAppInfo))
            await message.answer("Привет! Это бот твоей любимой кофейни! Нажми на кнопку снизу, чтобы заказать кофе!",
                                 reply_markup=builder.as_markup())
            await message.answer(str(message.from_user.id))
        else:
            await message.answer("С возвращением! Рады видеть вас снова!")
    else:
        await message.answer("Привет! Готов варить вкусный кофе?")
        


# @rt.message()
# async def send_order(message: Message):
#     """Handle '/start' command """
#     if (message.text == "1"):
#         builder = InlineKeyboardBuilder()
#         builder.button(text = 'Принять ✅',callback_data=OrderCallbackData(state=True, tg_id=message.from_user.id))
#         builder.button(text = 'Отклонить 🚫',callback_data=OrderCallbackData(state=False, tg_id=message.from_user.id))
#         data = [
#     {
#         "title": "Американо",
#         "size": 300,
#         "addons": [
#             {
#                 "title": "Сироп 1",
#                 "amount": 1
#             },
#             {
#                 "title": "Сироп 3",
#                 "amount": 1
#             },
#             {
#                 "title": "Сахар",
#                 "amount": 1
#             }
#         ],
#         "price": 249,
#         "amount": 1,
#         "id": 1
#     },
#     {
#         "title": "Латте",
#         "size": 300,
#         "addons": [
#             {
#                 "title": "Сироп 1",
#                 "amount": 1
#             },
#             {
#                 "title": "Сироп 3",
#                 "amount": 1
#             },
#             {
#                 "title": "Сахар",
#                 "amount": 1
#             }
#         ],
#         "price": 289,
#         "amount": 1,
#         "id": 2
#     }
#     ]
#         await bot.send_message(os.getenv("BARISTA_ID"), f'Пришел новый заказ!')
#         order = ""
#         for item in data:
#             order += f'{item["title"]} {item["size"]} мл\n'
#             for addon in item['addons']:
#                 order +=f'Добавить {addon["amount"]} {addon["title"]} '
        
#             order+= '\n'
#         await bot.send_message(os.getenv("BARISTA_ID"),order,reply_markup=builder.as_markup())
#         await message.reply("Ваш заказ создан! Ожидайте подтверждения!")

        #await bot.send_message(chat_id=os.getenv('bots_chat_id'), text="Новый заказ!")

@rt.callback_query(OrderCallbackData.filter(F.state == True))
async def order_accepted(query:CallbackQuery, callback_data: OrderCallbackData):
     await bot.send_message(callback_data.tg_id, "Ваш заказ скоро будет готов!")
     await bot.send_message(os.getenv("BARISTA_ID"))

async def getOrders():
    logging.info("Getting actual orders")
    orders = None
    async with async_session() as session:
        result = await session.execute(select(Orders).where(Orders.isaccepted==0))
        orders = result.scalars().all()
        for order in orders:
             logging.info(order.id)
             logging.info(order.odata)
    return orders 
                    
async def getOrderHTML(order):
     pass

@rt.message(F.text == 'Заказы')
async def order_window(message: Message):
    if (str(message.from_user.id) == os.getenv("BARISTA_ID")):
        logger.info("barista called orders message")
        orders = await getOrders()

        # for order in orders["data"]:
        #      text = getOrderHTML(order)
        #      await bot.send_message(int(os.getenv("BARISTA_ID")),)
        





async def main():
    try:
        logger.info("Starting bot...")
        await bot.delete_webhook(drop_pending_updates = True)
        await dp.start_polling(bot)
        await async_main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Bot stopped")

if __name__ == '__main__': # Corrected the if statement.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually")