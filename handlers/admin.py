import asyncio
from sys import platform

import pyrogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import config
from bot import bot
from database.admin import Admin_data_class
from database.chats import Chat_data_class
from database.stat_word import Stat_data_class
from other import func
from other import keyboard
from state.states import *

if platform == 'win32':
    string_key_word = 'data\\key_word.txt'
    string_dop_word = 'data\\dop_word.txt'
    string_stat = 'data\\stat.txt'
else:
    string_key_word = 'data/key_word.txt'
    string_dop_word = 'data/dop_word.txt'
    string_stat = 'data/stat.txt'

Admin_data = Admin_data_class()
Chat_data = Chat_data_class()
Stat_data = Stat_data_class()

client_pyrogram = pyrogram.Client("my_account", config.API_ID, config.API_HASH)


@client_pyrogram.on_message(pyrogram.filters.chat(Chat_data.get_chat_id()))
async def my_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    chat_id = message.chat.id
    message_id = message.id
    try:
        username = message.chat.username
        link = f't.me/{username}/{message_id}'
    except:
        link = f't.me/{str(chat_id).replace("-100", "")}/{message_id}'

    await asyncio.sleep(10)
    check_msg = await client.get_messages(chat_id, message_id)
    message_text = check_msg.text

    if message_text == None or check_msg.from_user.is_bot:
        return
    result = func.check_text(message_text)
    if result:
        await bot.send_message(config.CHAT_ID, f'<b>Нашел новый заказ:</b>\n\n'
                                               f'Ссылка: {link}\n'
                                               f'Ключевое слово: {result[1]}\n'
                                               f'Отправил: {check_msg.from_user.first_name} - @{check_msg.from_user.username}\n'
                                               f'Полный текст👇', parse_mode='HTML',
                               reply_markup=keyboard.rating_key_word(result[1]),
                               disable_web_page_preview=True)
        await bot.send_message(config.CHAT_ID, message_text)


async def show_panel(message: Message, state: FSMContext):
    '''Показываем админ панель'''
    await state.finish()
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        await message.answer('Вот твоя админ панель', reply_markup=keyboard.admin_panel())


async def rating_word(call: CallbackQuery, state: FSMContext):
    '''Статистика по словам'''
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        rating = call.data.split('_')[0]
        word = call.data.split('_')[1]
        Stat_data.add_word(word)
        if rating == 'bad':
            Stat_data.plus_bad(word)
            await call.answer(f'Ты 👎 слово {word}')
        elif rating == 'good':
            Stat_data.plus_good(word)
            await call.answer(f'Ты 👍 слово {word}')


async def get_rating_word(call: CallbackQuery, state: FSMContext):
    '''Получаем статистику по словам'''
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        Stat_data.update_stat()
        await call.bot.send_document(user_id, open(string_stat, 'rb'))


async def change_key_word(call: CallbackQuery, state: FSMContext):
    '''Меняем ключевые слова'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await call.message.answer('Пришли txt файл содержащий ключевые слова\n\n'
                                  'Слова должны быть перечислены через запятую.')
        await FSM_KEY_WORD.file.set()


async def change_key_word2(message: Message, state: FSMContext):
    '''Меняем ключевые слова (Загружаем файл с ключевыми словами)'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        if message.content_type == 'document':
            await message.document.download(string_key_word)
            await message.answer('Новые ключевые слова сохранены')
            await state.finish()
        else:
            await message.answer('Ты должен отправить файл')


async def get_key_word(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        with open(string_key_word, 'rb') as file:
            await call.bot.send_document(user_id, file)


async def change_dop_word(call: CallbackQuery, state: FSMContext):
    '''Меняем дополнительные слова'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await call.message.answer('Пришли txt файл содержащий дополнительные слова\n\n'
                                  'Слова должны быть перечислены через запятую.')
        await FSM_DOP_WORD.file.set()


async def change_dop_word2(message: Message, state: FSMContext):
    '''Меняем доп слова (Загружаем файл с доп словами)'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        if message.content_type == 'document':
            await message.document.download(string_dop_word)
            await message.answer('Новые дополнительные слова сохранены')
            await state.finish()
        else:
            await message.answer('Ты должен отправить файл')


async def get_dop_word(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        with open(string_dop_word, 'rb') as file:
            await call.bot.send_document(user_id, file)


async def add_chat(call: CallbackQuery, state: FSMContext):
    '''Добавляем чат'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await call.message.answer('Пришли мне ссылку на чат или канал')
        await FSM_ADD_CHAT.chat.set()


async def add_chat2(message: Message, state: FSMContext):
    '''Добавялем чат (записываем в бд и подписываемся)'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        try:
            await client_pyrogram.join_chat(message.text)  # присоединение к чату
            chat = await client_pyrogram.get_chat(message.text)
            Chat_data.add_chat(chat.id, message.text)
            await message.answer(f'Канал {chat.title} добавлен')
            await state.finish()
        except Exception as e:
            await message.answer(f'Не получилось добавить канал {e}')
            await state.finish()


async def del_chat(call: CallbackQuery, state: FSMContext):
    '''Удаляем чат'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await call.message.answer('Пришли мне ссылку канала/чата который надо удалить')
        await FSM_DELETE_CHAT.chat.set()


async def del_chat2(message: Message, state: FSMContext):
    '''Удаляем чат (убираем из бд и отписываемся)'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        try:
            chat = await client_pyrogram.get_chat(message.text)
            await client_pyrogram.leave_chat(chat.id)  # удаляем чат
            Chat_data.del_chat(chat.id)
            await message.answer(f'Канал {chat.title} удален')
            await state.finish()
        except Exception as e:
            await message.answer(f'Не получилось удалить канал {e}')
            await state.finish()


async def get_chats(call: CallbackQuery, state: FSMContext):
    '''Получаем список ссылок всех чатов'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        data = Chat_data.get_chat()
        text = 'Все чаты\n\n'
        for link in data:
            text += f'{link}\n'
        await call.message.answer(text)


async def add_admin(call: CallbackQuery, state: FSMContext):
    '''Добавляем админа'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await FSM_ADD_ADMIN.admin_id.set()
        await call.message.answer('Отправь мне id нового админа')

async def add_admin2(message: Message, state: FSMContext):
    '''Добавляем админа'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        if message.text.isdigit():
            Admin_data.add_admin(int(message.text))
            await message.answer('Новый админ добавлен')
            await state.finish()
        else:
            await message.answer('Нужно ID пользователя!!\n'
                                 'Получить его можно переслав сообщение от юзера в бота https://t.me/getmyid_bot')
            await state.finish()


async def del_admin(call: CallbackQuery, state: FSMContext):
    '''Удаляем админа'''
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in Admin_data.get_admins():
        await FSM_DEL_ADMIN.admin_id.set()
        await call.message.answer('Отправь мне id админа которого надо удалить')

async def del_admin2(message: Message, state: FSMContext):
    '''Удаляем админа'''
    user_id = message.from_user.id
    if user_id in Admin_data.get_admins():
        if message.text.isdigit():
            Admin_data.del_admin(int(message.text))
            await message.answer('Админ удален')
            await state.finish()
        else:
            await message.answer('Нужно ID пользователя!!\n'
                                 'Получить его можно переслав сообщение от юзера в бота https://t.me/getmyid_bot')
            await state.finish()


client_pyrogram.start()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(show_panel, commands='panel', state='*')
    dp.register_callback_query_handler(rating_word,
                                       lambda call: call.data.startswith('good_') or call.data.startswith('bad_'),
                                       state='*')
    dp.register_callback_query_handler(get_rating_word, lambda call: call.data == 'get_stat_words', state='*')

    dp.register_callback_query_handler(change_key_word, lambda call: call.data == 'set_key_words', state='*')
    dp.register_message_handler(change_key_word2, content_types=['document', 'text'], state=FSM_KEY_WORD.file)
    dp.register_callback_query_handler(get_key_word, lambda call: call.data == 'get_key_words', state='*')

    dp.register_callback_query_handler(change_dop_word, lambda call: call.data == 'set_dop_words', state='*')
    dp.register_message_handler(change_dop_word2, content_types=['document', 'text'], state=FSM_DOP_WORD.file)
    dp.register_callback_query_handler(get_dop_word, lambda call: call.data == 'get_dop_words', state='*')

    dp.register_callback_query_handler(add_chat, lambda call: call.data == 'add_chat', state='*')
    dp.register_message_handler(add_chat2, state=FSM_ADD_CHAT.chat)
    dp.register_callback_query_handler(del_chat, lambda call: call.data == 'del_chat', state='*')
    dp.register_message_handler(del_chat2, state=FSM_DELETE_CHAT.chat)
    dp.register_callback_query_handler(get_chats, lambda call: call.data == 'get_chat', state='*')

    dp.register_callback_query_handler(add_admin, lambda call: call.data == 'add_admin', state='*')
    dp.register_message_handler(add_admin2, state=FSM_ADD_ADMIN.admin_id)

    dp.register_callback_query_handler(del_admin, lambda call: call.data == 'del_admin', state='*')
    dp.register_message_handler(del_admin2, state=FSM_DEL_ADMIN.admin_id)
