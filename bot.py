from telebot.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from configs import TELEGRAM_API_TOKEN
from image import put_text
from time import sleep
import telebot
import os


bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
user_form_types: dict = {}
user_post_types: dict = {}
user_question_rounds: dict = {}

user_game_info: dict = {}
user_final_info: dict = {}

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=1)
    row = [KeyboardButton(x) for x in ["Normal Post (Uncensored)", "Normal Post (Censored)"]]
    markup.add(*row)
    
    return markup

def form_markup():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Single Match", callback_data="single")
    button2 = InlineKeyboardButton("Double Matches", callback_data="double")
    button3 = InlineKeyboardButton("Triple Matches", callback_data="triple")

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    return markup

def format_to_dict(postType: int, formType: int, game_info:list[tuple]):
    if postType == 1:
        info = {
            "is_blurred" : False,
            "form_type" : formType,
            "game_info" : game_info
        }

        return info

    elif postType == 2:
        info = {
            "is_blurred" : True,
            "form_type" : formType,
            "game_info" : game_info
        }

        return info
   
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,"Please select what you post type is ...",reply_markup=keyboard())

@bot.message_handler(func=lambda message:True)
def all_messages(message: Message):
    user_post_types[message.from_user.id] = 1

    if message.text == "Normal Post (Uncensored)":
        user_post_types[message.from_user.id] = 1
    
    elif message.text == "Normal Post (Censored)":
        user_post_types[message.from_user.id] = 2
        
    bot.send_message(message.chat.id, f"You Selected {message.text}", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Ok, Now Please Select Which Form Type You Want ...", reply_markup=form_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data == "single":
        user_form_types[call.from_user.id] = 1
    elif call.data == "double":
        user_form_types[call.from_user.id] = 2
    elif call.data == "triple":
        user_form_types[call.from_user.id] = 3

    user_question_rounds[call.from_user.id] = 0
    ask_date(call.message, call.from_user.id)

    user_game_info[call.from_user.id] = [list() for _ in range(user_form_types[call.from_user.id])]

def ask_date(message, user_id):
    bot.reply_to(message, "Now please Send The Date Of The Match \nfor example 15-july")
    bot.register_next_step_handler(message, process_date, user_id)

def process_date(message, user_id):
    user_game_info[user_id][user_question_rounds[user_id]].append(message.text)
    ask_leagues(message, user_id)

def ask_leagues(message, user_id):
    bot.reply_to(message, "Now please Send The Leagues In The Match \nfor example England - Championship")
    bot.register_next_step_handler(message, process_leagues, user_id)

def process_leagues(message, user_id):
    user_game_info[user_id][user_question_rounds[user_id]].append(message.text)
    ask_teams(message, user_id)

def ask_teams(message, user_id):
    bot.reply_to(message, "Now please Send The Teams In The Match \nfor example Manchester City - Arsenal")
    bot.register_next_step_handler(message, process_teams, user_id)

def process_teams(message, user_id):
    user_game_info[user_id][user_question_rounds[user_id]].append(message.text)
    ask_events_odds(message, user_id)

def ask_events_odds(message, user_id):
    bot.reply_to(message, "Now please Send The Team event : odd \nfor example 1-2:3.4")
    bot.register_next_step_handler(message, process_events_odds, user_id)

def process_events_odds(message, user_id):
    user_game_info[user_id][user_question_rounds[user_id]].append(message.text)
    user_question_rounds[user_id] += 1

    check_round_completion(message, user_id)

def check_round_completion(message, user_id):
    if user_question_rounds[user_id] < user_form_types[user_id]:
        ask_date(message, user_id)  # Restart the question sequence for the next round
    
    if (user_question_rounds[user_id] == user_form_types[user_id]) == True:
        final_info = format_to_dict(user_post_types[user_id], user_form_types[user_id], user_game_info[user_id])
        put_text(str(user_id), final_info)
        
        bot.send_photo(chat_id=message.chat.id, photo=open(f"{user_id}.jpg", "rb"))
        
        sleep(1.5)

        os.remove(f"{user_id}.jpg")

bot.infinity_polling(timeout=None)

