from config import Config
from telebot import TeleBot
from telebot.types import Message, CallbackQuery


from storage.sqlite import SQLiteStorage 
from service.user_service import UserService
from service.category_service import CategoryService
from service.operation_service import OperationService

# logger = telebot.logger
# formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#                                   '%m-%d %H:%M:%S')
# ch = logging.StreamHandler(sys.stdout)
# logger.addHandler(ch)
# logger.setLevel(logging.DEBUG)  # or use logging.INFO
# ch.setFormatter(formatter)

cfg = Config('config.yaml')
bot = TeleBot(cfg.API_TOKEN)
storage = SQLiteStorage(cfg.DATABASE_NAME)
user_service = UserService(storage=storage)
category_service = CategoryService(storage=storage)
operation_service = OperationService(storage=storage)
operation_query = {}


@bot.message_handler(commands=['start'])
def start_message(message: Message):
  bot.send_message(message.chat.id, "Введи команду", reply_markup=user_service.get_menu_keyboard())

@bot.message_handler(commands=['cancel'])
def start_message(message: Message):
  bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
  bot.send_message(message.chat.id, "Отмена")

@bot.message_handler(commands=['reg'])
def register_user(message: Message):
  user_service.register(message.from_user.id)
  bot.send_message(message.chat.id, "Аккаунт зарегистрован")

@bot.message_handler(commands=['add_category'])
def add_category(message: Message):
  bot.send_message(message.chat.id, "Пришли мне название категории")
  bot.register_next_step_handler(message, category_service.add_category_handler, bot)

@bot.message_handler(commands=['delete_category'])
def delete_category(message: Message):
  bot.send_message(
    message.chat.id,
    "Выбери категорию",
    reply_markup=category_service.get_keyboard(message.from_user.id)
  )

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_category'))    
def callback_delete_category(call: CallbackQuery):
  category_service.delete_category(call.from_user.id, call.data.split("_")[2].lower())
  bot.send_message(call.message.chat.id, "Категория удалена")
  bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['add_operation'])
def add_operation(message: Message):
  operation_query[message.from_user.id] = {}
  bot.send_message(
    message.chat.id,
    "Выбери категорию",
    reply_markup=operation_service.get_category_keyboard(message.from_user.id)
  )

@bot.callback_query_handler(func=lambda call: call.data.startswith('category_operation'))    
def callback_category_operation(call: CallbackQuery):
  operation_query[call.from_user.id] = {}
  operation_query[call.from_user.id]['category'] = call.data.split("_")[2].lower()
  bot.delete_message(call.message.chat.id, call.message.message_id)
  bot.send_message(call.message.chat.id, "Количество денег")
  bot.register_next_step_handler(call.message, amount_operation)

def amount_operation(message: Message):
  operation_query[message.from_user.id]['amount'] = message.text
  bot.delete_message(message.chat.id, message.message_id)
  bot.delete_message(message.chat.id, message.message_id-1)
  bot.send_message(
    message.chat.id, 
    "Добавить описание операции?", 
    reply_markup=operation_service.get_description_keyboard()
  )

@bot.callback_query_handler(func=lambda call: call.data.startswith('desc_true'))
def callback_desc_1(call: CallbackQuery):
  bot.delete_message(call.chat.id, call.message.message_id)
  bot.send_message(call.message.chat.id, "Опиши операцию")
  bot.register_next_step_handler(call.message, description_operation)

@bot.callback_query_handler(func=lambda call: call.data.startswith('desc_false'))
def callback_desc_2(call: CallbackQuery):
  operation_query[call.from_user.id]['description'] = 'без описания'
  bot.delete_message(call.message.chat.id, call.message.message_id)
  bot.send_message(
      call.message.chat.id,
      "Получил или потратил?",
      reply_markup=operation_service.get_enrollment_keyboard()
    )
    
def description_operation(message: Message):
  operation_query[message.from_user.id]['description'] = message.text
  bot.delete_message(message.chat.id, message.message_id)
  bot.send_message(
    message.chat.id,
    "Получил или потратил?",
    reply_markup=operation_service.get_enrollment_keyboard()
  )
  
@bot.callback_query_handler(func=lambda call: call.data.startswith('enroll_true'))
def callback_enroll_true(call: CallbackQuery):
  operation_query[call.from_user.id]['is_enrollment'] = '1'
  bot.delete_message(call.message.chat.id, call.message.message_id)
  operation_service.add_operation(
    call.from_user.id,
    operation_query[call.from_user.id]['category'],
    operation_query[call.from_user.id]['description'],
    operation_query[call.from_user.id]['amount'],
    operation_query[call.from_user.id]['is_enrollment']
  )
  bot.send_message(
    call.message.chat.id, 
    "Операция добавлена:\n{category}-{description}-{amount}-получил".format(
      category=operation_query[call.from_user.id]['category'],
      description=operation_query[call.from_user.id]['description'],
      amount=operation_query[call.from_user.id]['amount']
      )
  )

@bot.callback_query_handler(func=lambda call: call.data.startswith('enroll_false'))
def callback_enroll_false(call: CallbackQuery):
  operation_query[call.from_user.id]['is_enrollment'] = '0'
  bot.delete_message(call.message.chat.id, call.message.message_id)
  operation_service.add_operation(
    call.from_user.id,
    operation_query[call.from_user.id]['category'],
    operation_query[call.from_user.id]['description'],
    operation_query[call.from_user.id]['amount'],
    operation_query[call.from_user.id]['is_enrollment']
  )
  bot.send_message(
    call.message.chat.id, 
    "Операция добавлена:\n{category}-{description}-{amount}-потратил".format(
      category=operation_query[call.from_user.id]['category'],
      description=operation_query[call.from_user.id]['description'],
      amount=operation_query[call.from_user.id]['amount']
      )
  )

if __name__ == '__main__':
  bot.infinity_polling()