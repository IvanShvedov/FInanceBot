from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from storage.base_storage import Storage
from service.queries import ADD_OPERATION, GET_ALL_CATEGORIES

class OperationService:

    def __init__(self, storage: Storage):
        self.storage = storage
    
    def add_operation(
            self,
            user_telegram_id: str, 
            category_name: str, 
            description: str,
            amount: str,
            is_enrollment: str
        ):
        self.storage.execute(
            ADD_OPERATION.format(
                user_telegram_id=user_telegram_id,
                category_name=category_name,
                description=description,
                amount=amount,
                is_enrollment=is_enrollment
                )
        )

    def get_all_categories(self, user_telegram_id: str):
        return self.storage.fetch(GET_ALL_CATEGORIES.format(user_telegram_id=user_telegram_id))

    def get_category_keyboard(self, user_telegram_id: str):
        markup = InlineKeyboardMarkup()
        for row in self.get_all_categories(user_telegram_id):
            markup.add(InlineKeyboardButton(
                text=row[1],
                callback_data='category_operation_' + row[1]
            ))
        return markup

    def get_description_keyboard(self):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Да', callback_data='desc_true'))
        markup.add(InlineKeyboardButton(text='Нет', callback_data='desc_false'))
        return markup

    def get_enrollment_keyboard(self):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Потратил', callback_data='enroll_false'))
        markup.add(InlineKeyboardButton(text='Получил', callback_data='enroll_true'))
        return markup
    