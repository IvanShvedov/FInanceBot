from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from storage.base_storage import Storage
from service.queries import DOES_EXIST_CATEGORY, ADD_CATEGORY, DELETE_CATEGORY, GET_ALL_CATEGORIES

class CategoryService:

    def __init__(self, storage: Storage):
        self.storage = storage

    def does_exist(self, user_telegram_id: str, category_name: str):
        res = self.storage.fetch(
            DOES_EXIST_CATEGORY.format(
                user_telegram_id=user_telegram_id,
                category_name=category_name
                )
            )
        return res

    def add_category(self, user_telegram_id: str, category_name: str):
        if not self.does_exist(user_telegram_id, category_name):
            self.storage.execute(
                ADD_CATEGORY.format(
                    user_telegram_id=user_telegram_id,
                    category_name=category_name
                    )
            )
    
    def delete_category(self, user_telegram_id: str, category_name: str):
        if self.does_exist(user_telegram_id, category_name):
            self.storage.execute(
                DELETE_CATEGORY.format(
                    user_telegram_id=user_telegram_id,
                    category_name=category_name
                    )
            )

    def get_all_categories(self, user_telegram_id: str):
        return self.storage.fetch(GET_ALL_CATEGORIES.format(user_telegram_id=user_telegram_id))
        
    def add_category_handler(self, message: Message, bot):
        self.add_category(message.from_user.id, message.text.lower())
        bot.send_message(message.chat.id, "Категория добавлена")

    def get_keyboard(self, user_telegram_id: str):
        markup = InlineKeyboardMarkup()
        for row in self.get_all_categories(user_telegram_id):
            markup.add(InlineKeyboardButton(
                text=row[1],
                callback_data='delete_category_' + row[1]
            ))
        return markup
            