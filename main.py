from aiogram.utils import executor

import config
from bot import bot, dp
from database.admin import Admin_data_class
from handlers.admin import register_admin

Admin_data = Admin_data_class()


async def main(_):  # Функция выполняется при запуске
    for admin in Admin_data.get_admins():
        try:
            await bot.send_message(admin, 'Бот запущен!')

        except:
            pass
    await bot.send_message(config.CHAT_ID, 'Бот запущен!')


register_admin(dp)
executor.start_polling(dp, on_startup=main)
