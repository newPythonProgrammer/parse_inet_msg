import gspread
from sys import platform

if platform == 'win32':
    string_key_word = 'data\\key_word.txt'
    string_dop_word = 'data\\dop_word.txt'
    string_stop_list = 'data\\stop_word.txt'
else:
    string_key_word = 'data/key_word.txt'
    string_dop_word = 'data/dop_word.txt'
    string_stop_list = 'data/stop_word.txt'
def add_msg_table_main(key_word, sender, text_msg, chat, chat_title, msg_link):
    gc = gspread.service_account(filename='parse.json')
    sheet = gc.open_by_key('1Cr8mRhfp8HFyOIoRckof2E7yBIRj34SuQs6QWN09Kx8')
    worksheet = sheet.worksheet(title='Целевые')
    for i in range(2,9999999999):
        val = worksheet.acell(f'A{i}').value
        if val == None:
            check = worksheet.acell(f'B{i}').value
            if check == None:
                break
    worksheet.update(f'A{i}', key_word)
    worksheet.update(f'B{i}', sender)
    worksheet.update(f'C{i}', text_msg)
    worksheet.update(f'D{i}', chat)
    worksheet.update(f'E{i}', chat_title)
    worksheet.update(f'F{i}', msg_link)


def add_msg_table_dop(key_word, sender, text_msg, chat, chat_title, msg_link):
    gc = gspread.service_account(filename='parse.json')
    sheet = gc.open_by_key('1Cr8mRhfp8HFyOIoRckof2E7yBIRj34SuQs6QWN09Kx8')
    worksheet = sheet.worksheet(title='дополнительные')
    for i in range(2,9999999999):
        val = worksheet.acell(f'A{i}').value
        if val == None:
            check = worksheet.acell(f'B{i}').value
            if check == None:
                break
    worksheet.update(f'A{i}', key_word)
    worksheet.update(f'B{i}', sender)
    worksheet.update(f'C{i}', text_msg)
    worksheet.update(f'D{i}', chat)
    worksheet.update(f'E{i}', chat_title)
    worksheet.update(f'F{i}', msg_link)


def check_text(text:str) -> bool or tuple:
    '''Функция которая определяет есть ли ключевое слово в тексте'''
    text = text.lower()#уменьшаем текст

    with open(string_stop_list, 'r', encoding='utf-8') as stop_words_file:#открываем файл с стоп словами
        stop_words_list = stop_words_file.read().lower().split(',')#составляем список стоп слов
        word_list_stop = []
        for word in stop_words_list:
            if len(word) <3:
                continue
            word_list_stop.append(word.strip())#пополняем список стоп слов

    for stop_word in word_list_stop:
        if stop_word in text:
            return False #Если есть стоп слово в тексте то сразу возвращаем False



    with open(string_key_word, 'r', encoding='utf-8') as key_words_file:#открываем файл с ключевыми словами
        key_words_list = key_words_file.read().lower().split(',')#составляем список ключевых слов
        word_list = []
        for word in key_words_list:
            # if len(word) < 3:
            #     continue
            word_list.append(word.strip()) #пополняем список ключевых слов
    for key_word in word_list:
        if key_word in text:#Если ключевое слово есть в тексте
            return ('key', key_word)

    with open(string_dop_word, 'r', encoding='utf-8') as dop_words_file:#открываем файл с доп словами
        dop_words_list = dop_words_file.read().lower().split(',')#составляем список доп слов
        word_list = []
        for word in dop_words_list:
            if len(word) < 3:
                continue
            word_list.append(word.strip()) #пополняем список доп слов
    for dop_word in word_list:
        if dop_word in text:#Если доп слово есть в тексте
            return ('dop', dop_word)

    return False


