import sqlite3
from sys import platform

if platform == 'win32':
    string_db = 'data\\admin.db'
else:
    string_db = 'data/admin.db'


class Admin_data_class:
    '''Класс для управления БД админов'''

    def __init__(self):
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS admin(
            Admin_ID INTEGER)''')

    def add_admin(self, admin_id):
        '''Добавляем админа'''
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM admin WHERE Admin_ID = ?''', (admin_id,))
            checker = cursor.fetchone()
            if not checker:
                cursor.execute('''INSERT INTO admin(Admin_ID) VALUES(?)''', (admin_id,))

    def del_admin(self, admin_id):
        '''Удаляем админа'''
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''DELETE FROM admin WHERE Admin_ID = ?''', (admin_id,))

    def get_admins(self):
        '''получаем список админов'''
        with sqlite3.connect(string_db) as connect:
            cursor = connect.cursor()
            cursor.execute('''SELECT * FROM admin''')
            data = cursor.fetchall()
            result = []
            for i in data:
                result.append(i[0])
            return result