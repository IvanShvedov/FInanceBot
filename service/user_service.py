from telebot.types import ReplyKeyboardMarkup

from storage.base_storage import Storage
from service.queries import DOES_EXIST_USER, REGISTER_USER

class UserService:

    def __init__(self, storage: Storage):
        self.storage = storage

    def does_exist(self, user_telegram_id: str):
        res = self.storage.fetch(
            DOES_EXIST_USER.format(user_telegram_id=user_telegram_id)
            )
        return res

    def register(self, user_telegram_id: str):
        if not self.does_exist(user_telegram_id):
            self.storage.execute(
                REGISTER_USER.format(user_telegram_id=user_telegram_id)
            )
    
    def get_menu_keyboard(self):
        markup = ReplyKeyboardMarkup()
        markup.row('/reg', '/cancel')
        markup.row('/add_category', '/delete_category')
        markup.row('/add_operation')
        return markup