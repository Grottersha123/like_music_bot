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


def create_button(data, count_like, count_dislike):
    kb1 = InlineKeyboardMarkup()
    for i in data['inline_keyboard']:
        button1, button2 = i
        button1['text'] = text_btn1 + ' ' + str(count_like)
        button2['text'] = text_btn2 + ' ' + str(count_dislike)
        kb1.add(InlineKeyboardButton(**button1), InlineKeyboardButton(**button2))
    return kb1

def statistic_update(db, message_id):
    count = db.get(str.encode(message_id))
    count = int(count or 0) + 1
    db.put(str.encode(message_id), str.encode(str(count)))
    return count


def get_count(db, message_id):
    count = db.get(str.encode(message_id))
    return int(count or 0)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global count_1
    global count_2
    global inline_kb1
    code = callback_query.data[-1]
    message_id = callback_query.message.message_id
    user = callback_query.from_user.username
    if code.isdigit():
        code = int(code)
    users = db.get(str.encode(str(message_id)+'u'))
    if user not in str(users or ''):
        db.put(str.encode(str(message_id)+'u'), str.encode(str(users or '')+'_'+user))
        if code == 1:
            count_l = statistic_update(db, str(message_id)+'l')
            count_d = get_count(db, str(message_id)+'d')
            # kb1.add(InlineKeyboardButton(**button1), InlineKeyboardButton(**button2))
        if code == 2:
            count_d = statistic_update(db, str(message_id) + 'd')
            count_l = get_count(db, str(message_id)+'l')

        data = inline_kb1.as_json()
        data = ast.literal_eval(data)
        kb1 = create_button(data, count_l, count_d)

        await bot.edit_message_reply_markup(message_id=callback_query.message.message_id,
                                        chat_id=callback_query.message.chat.id, reply_markup=kb1)
    else:
        await bot.answer_callback_query(callback_query.id, text='вы уже голосовали')


@dp.message_handler()
async def any_text_message(message: types.Message):
    if not message.from_user.is_bot:
        await message.reply(message.text, reply_markup=inline_kb1)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
