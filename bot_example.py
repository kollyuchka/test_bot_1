# # -*- coding: utf-8 -*-
import telebot
import asyncio
from flask import Flask
from flask import request
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
import config
from additional_functions import keyboard_start,keyboard_second,save_name,get_name
from additional_functions import save_credit_story_bank,check_name,save_tech_support
import re

bot = telebot.TeleBot(config.TOKEN)
bot.remove_webhook()
bot.set_webhook(config.URL)
action_endpoint = config.ACTION_ENDPOINT
agent1 = Agent.load('./models/20210805-150623.tar.gz', action_endpoint=EndpointConfig(action_endpoint))


async def process(agent, msg):
    output = await agent.handle_text(msg)
    return output[0]['text']


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return {"ok": True}


@bot.message_handler(content_types=['text'])
def text_command(message):
    mess = asyncio.run(process(agent1, message.text))
    name = re.findall(r'\Приятно познакомиться, (.*?)\!', mess)
    greet = re.findall(r'(\Привет)',mess)
    bank  = re.findall(r'Банк (.*?) С',mess)
    summa  = re.findall(r'[0-9]{3,10}',mess)
    question = re.findall(r'(\вопрос)',mess)


    if len(name)>0:
             save_name(name[0])
             bot.send_message(message.chat.id, f" Привет,{get_name()}. Что Вас интересует?",reply_markup=keyboard_start)
    elif (check_name()==False and len(greet)>0 ) :
             bot.send_message(message.chat.id, f"Привет,как тебя зовут.")
    elif (check_name()==True and len(greet)>0 ):
        bot.send_message(message.chat.id, f" Привет,{get_name()}. Что Вас интересует?",reply_markup=keyboard_start)

    elif len(summa)>0:
        save_credit_story_bank(bank[0],summa[0])
        bot.send_message(message.chat.id,mess)

    elif len(question)>0:
        save_tech_support(message.text)
        bot.send_message(message.chat.id,mess)
    else:
        bot.send_message(message.chat.id,mess)



@bot.callback_query_handler(func=lambda call: True)
def callback_workr(call):
    if call.data == "first_step_tech":
        bot.send_message(call.message.chat.id, "Напишиту! Что Вас интересует?:\nBug\nNew feature\nOther")
    if call.data == "first_step_credit":
        bot.send_message(call.message.chat.id, text="Выберете что вам нужно:", reply_markup=keyboard_second)
    if call.data == "credit_new":
        bot.send_message(call.message.chat.id, "Напишите! Наименование банка :\notpbank,\nСберБанк,\nАльфа-банк\n и сумму кредита через пробел\nПример: СберБанк 500000)")
    if call.data == "credit_calculation":
            bot.send_message(call.message.chat.id, "ожидайте")
    if call.data == "back":
        bot.send_message(call.message.chat.id,f"Что Вас интересует?", reply_markup=keyboard_start)

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    bot.send_message(message.chat.id,f"Фото передано!")



if __name__ == "__main__":
    app.run(host="flask", port=5000)
