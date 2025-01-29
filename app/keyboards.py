from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Добавить пользователя', callback_data='birthday_data_add')],
    ],
    resize_keyboard=True
)

