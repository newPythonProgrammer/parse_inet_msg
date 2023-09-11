import sqlite3
from sys import platform

if platform == 'win32':
    string_db = 'data\\stat_word.db'
    string_stat = 'data\\stat.txt'
else:
    string_db = 'data/stat_word.db'
    string_stat = 'data/stat.txt'

class Stat_data_class:
    def __init__(self):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS stat(
            Word TEXT,
            Bad INTEGER DEFAULT 0,
            Good INTEGER DEFAULT 0)''')

    def add_word(self, word):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM stat WHERE Word = ?''', (word,))
            checker = cursor.fetchone()
            if not checker:
                cursor.execute('''INSERT INTO stat(Word) VALUES(?)''', (word,))

    def plus_bad(self, word):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE stat SET Bad = Bad+1 WHERE Word=?''', (word,))

    def plus_good(self, word):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''UPDATE stat SET Good = Good+1 WHERE Word=?''', (word,))

    def update_stat(self):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM stat''')
            data = cursor.fetchall()
            text = 'СЛОВО - МИНУСОВ - ПЛЮСОВ\n\n'
            for word, bad, good in data:
                text += f'{word} - {bad} - {good}\n'
            with open(string_stat, 'w', encoding='utf-8') as file:
                file.write(text)
