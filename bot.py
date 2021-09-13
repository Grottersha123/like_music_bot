import logging
from aiogram import Bot, Dispatcher, executor, types

from os import getenv

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot_token = getenv("BOT_TOKEN")
# Объект бота
bot = Bot(token=bot_token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)



inline_btn_1 = InlineKeyboardButton('Хороший трек', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('Ну, такое...', callback_data='button2')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    print(callback_query.message, callback_query.from_user.username)
    data = inline_kb1.as_json()
    print(type(data))
    kb1 = InlineKeyboardMarkup()
    for i in data['inline_keyboard']:
        print(i)
        kb1.add(InlineKeyboardButton(**i))



    if code.isdigit():
        code = int(code)
    if code == 1:
        await bot.edit_message_reply_markup(message_id=callback_query.message.message_id,
                                            chat_id=callback_query.message.chat.id, reply_markup=kb1)
    if code == 2:
        await bot.edit_message_reply_markup(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, reply_markup=kb1)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')



@dp.message_handler()
async def any_text_message(message: types.Message):
    print(message.message_id)
    # if not message.from_user.is_bot:
    await message.reply(message.text, reply_markup=inline_kb1)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)