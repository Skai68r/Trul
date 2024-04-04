from bot_settings import bot
import sqlite
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

def register_welcome_handlers():
    bot.register_message_handler(welcome, commands=['start'])
    bot.register_message_handler(welcome, commands=['menu'])
    bot.register_message_handler(list_variants, commands=['list'])
    bot.register_callback_query_handler(send_user_id_and_names, lambda call: call.data.startswith('show_'))
    bot.register_callback_query_handler(send_products_keyboard_edit, lambda call: call.data.startswith('back_to_categories'))
    bot.register_callback_query_handler(delete_message, lambda call: call.data.startswith('back'))
    bot.register_callback_query_handler(send_products_list, lambda call: call.data.startswith('send_'))
    bot.register_callback_query_handler(send_product_info, lambda call: call.data.startswith('product_info_'))
    bot.register_callback_query_handler(send_order_process, lambda call: call.data.startswith('order_'))
    bot.register_message_handler(welcome, regexp='🔙Назад')
    bot.register_message_handler(send_personal_area, regexp='👩🏻‍🚀Личный кабинет')
    bot.register_message_handler(send_manager, regexp='💬Менеджер')
    bot.register_message_handler(send_products_keyboard, regexp='📦Товары')


def send_order_process(call):
    # Здесь можно вставить процесс покупки через интернет эквайринг
    type = call.data[6:]
    now = datetime.now()
    id = 1
    sqlite.insert_order_to_base(type, call.from_user.id, now, "оплачено")

    bot.answer_callback_query(call.id, "Спасибо за оформление заказа, ожидайте сообщения от менеджера.", show_alert=True)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

def send_product_info(call):
    name = call.data[13:]
    description, price, image = sqlite.get_description_by_name(name)
    file = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"Купить {price} ₽", callback_data=f"order_{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_photo(call.from_user.id, file, description, reply_markup=markup)


def send_products_list(call):
    category = call.data[5:]
    products = sqlite.get_products_by_category(category)
    markup = InlineKeyboardMarkup()
    for product in products:
        markup.add(InlineKeyboardButton(text=f"{product[0]}", callback_data=f'product_info_{product[0]}'))
    markup.add(InlineKeyboardButton(text="Назад", callback_data='back_to_categories'))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

def send_products_keyboard_edit(call):
    send_products_keyboard(call, edit=True)



def send_products_keyboard(message, edit=False):
    image = open('images/main.png', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Сухоцветы", callback_data="send_dried"))
    markup.add(InlineKeyboardButton(text="Букеты в крафтовых пакетах", callback_data="send_bag"))
    text = "Цветочная мастерская для души"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)



def send_manager(message):
    text = '[Написать специалисту](https://t.me/skai68r)'
    bot.send_message(message.from_user.id, text, parse_mode='markdown')


def send_personal_area(message):
    # Перед этой функцией можно поставить авторизацию в личный кабинет через ввод логина и пароля
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Заказы"), KeyboardButton(text="Возврат"), KeyboardButton(text="Написать специалисту"))
    markup.add(KeyboardButton(text="История покупок"), KeyboardButton(text="🔙Назад"))
    bot.send_message(message.from_user.id, "Добро пожаловать в личный кабинет!", reply_markup=markup)




def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)



def welcome(message):
    sqlite.insert_user(message.from_user.id, message.from_user.first_name)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="📦Товары"), KeyboardButton(text="🫥О нас"), KeyboardButton(text="💬Менеджер"))
    markup.add(KeyboardButton(text="👩🏻‍🚀Личный кабинет"))
    bot.send_message(message.from_user.id, "Приветствую тебя в нашем магазине!", reply_markup=markup)

def list_variants(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="user_id", callback_data='show_users_id'),
               InlineKeyboardButton(text="names", callback_data='show_names'))

    bot.send_message(message.from_user.id, "Выбери формат списка: ", reply_markup=markup)


def send_user_id_and_names(call):
    data = call.data[5:]
    user_data = sqlite.get_user_id_and_name()   #хранит кортежи из айди и имен
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Назад", callback_data='back'))    #закрытие показанных списков
    text = f"*Список пользователей:*\n"
    number = 1
    for user_id, name in user_data:
        if data == 'users_id':
            text += f"{number}) {str(user_id)}\n"
        elif data == 'names':
            text += f"{number}) {name}\n"
        number += 1
    bot.send_message(call.from_user.id, text, parse_mode='markdown', reply_markup=markup)   #здесь запрашивает что выводить, айди или имена и выводит их, маркдаун в этой строке добавляет форматирование


