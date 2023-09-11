from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def disactive_status():
    menu = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Остановить прием заявок', callback_data='stop_status')
    menu.add(btn)
    return menu

def active_status():
    menu = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Возобновить прием заявок', callback_data='start_status')
    menu.add(btn)
    return menu


def admin_panel():
    menu = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Установить новые ключевые слова', callback_data='set_key_words')
    btn2 = InlineKeyboardButton(text='Получить ключевые слова', callback_data='get_key_words')
    btn3 = InlineKeyboardButton(text='Установить новые доп. слова', callback_data='set_dop_words')
    btn4 = InlineKeyboardButton(text='Получить доп. слова', callback_data='get_dop_words')
    btn5 = InlineKeyboardButton(text='Получить статистику по словам', callback_data='get_stat_words')
    btn6 = InlineKeyboardButton(text='Добавить чат/канал', callback_data='add_chat')
    btn7 = InlineKeyboardButton(text='Получить все чаты', callback_data='get_chat')
    btn8 = InlineKeyboardButton(text='Удалить чат', callback_data='del_chat')
    btn9 = InlineKeyboardButton(text='Добавить администратора', callback_data='add_admin')
    btn10 = InlineKeyboardButton(text='Удалить администратора', callback_data='del_admin')
    menu.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    return menu

def rating_key_word(word):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='👍', callback_data=f'good_{word}')
    btn2 = InlineKeyboardButton(text='👎', callback_data=f'bad_{word}')
    menu.add(btn1, btn2)
    return menu

