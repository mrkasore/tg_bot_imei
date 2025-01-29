from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.orm as db
import app.keyboards as kb
import app.api as api
import os

router = Router()

class AddUser(StatesGroup):
    id_user_telegram = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.create_user(message.from_user.id)
    if int(os.getenv('ADMIN_ID')) == message.from_user.id:
        await message.answer(f'Вы авторизованы как Админ! Введите IMEI устройства:', reply_markup = kb.main)
        await db.create_user(message.from_user.id)
    else:
        await message.answer(f'Привет, {str(message.from_user.full_name)}! Введите IMEI устройства:')
        await db.create_user(message.from_user.id)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        "Привет! Я бот для для проверки IMEI устройств.\n\n"
        "Вот список доступных команд:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справочную информацию\n"
    )

@router.message(F.text == 'Добавить пользователя')
async def add_birthday_event(message: Message, state: FSMContext):
    if int(os.getenv('ADMIN_ID')) == message.from_user.id:
        await message.answer('Введите Telegram ID пользователя:')
        await state.set_state(AddUser.id_user_telegram)
    else:
        await message.answer('Данная команда недоступна!')

@router.message(AddUser.id_user_telegram)
async def process_new_fio(message: Message, state: FSMContext):
    telegram_id = message.text
    await state.update_data(id_user=telegram_id)
    data = await state.get_data()
    id_user = data['id_user']
    if id_user.isnumeric():
        await db.create_user(id_user)
        await message.answer(f'Добавлен новый пользователь ID - {telegram_id}')
    else:
        await message.answer('Введен некорректный ID')
    await state.clear()

@router.message()
async def get_imei(message: Message):
    device_id = message.text
    if api.is_imei_valid(device_id):
        response = await api.get_response(device_id)
        await message.answer(response.text)
    else:
        await message.answer('Невалидниый IMEI')
    await message.answer('Введите IMEI устройства: ')
