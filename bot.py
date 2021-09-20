import logging
from aiogram import Bot, Dispatcher, executor, types
import plyvel
import ast
from os import getenv

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import text_btn1, text_btn2

bot_token = getenv("BOT_TOKEN")
# Объект бота
bot = Bot(token=bot_token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
db = plyvel.DB('db')

inline_btn_1 = InlineKeyboardButton(text_btn1, callback_data='button1')
inline_btn_2 = InlineKeyboardButton(text_btn2, callback_data='button2')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

count_1 = 0
count_2 = 0


def create_button(data, count_like, count_dislike):
    kb1 = InlineKeyboardMarkup()
    for i in data['inline_keyboard']:
        button1, button2 = i
        button1['text'] = button1['text'] + ' ' + str(count_like)
        button2['text'] = button2['text'] + ' ' + str(count_dislike)
        kb1.add(InlineKeyboardButton(**button1), InlineKeyboardButton(**button2))
    return kb1


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global count_1
    global count_2
    code = callback_query.data[-1]
    print(callback_query.message.message_id, callback_query.from_user.username, callback_query.message.chat.id)
    data = inline_kb1.as_json()
    kb1 = InlineKeyboardMarkup()
    data = ast.literal_eval(data)
    for i in data['inline_keyboard']:
        button1, button2 = i
        kb1.add(InlineKeyboardButton(**button1), InlineKeyboardButton(**button2))
    print(kb1)
    if code.isdigit():
        code = int(code)
    if code == 1:
        # kb1.add(InlineKeyboardButton(**button1), InlineKeyboardButton(**button2))
        count_1 += 1
    if code == 2:
        count_2 += 1
    else:
        await bot.answer_callback_query(callback_query.id)
    kb1 = create_button(data, count_1, count_2)
    await bot.edit_message_reply_markup(message_id=callback_query.message.message_id,
                                        chat_id=callback_query.message.chat.id, reply_markup=kb1)


@dp.message_handler()
async def any_text_message(message: types.Message):
    print(message.message_id)
    # if not message.from_user.is_bot:
    await message.reply(message.text, reply_markup=inline_kb1)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
