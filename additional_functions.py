from telebot import types
import json
import os
keyboard_start = types.InlineKeyboardMarkup()
credit_works = types.InlineKeyboardButton(text='Работа с кредитами', callback_data='first_step_credit')
technical_support= types.InlineKeyboardButton(text='Запрос в тех поддержку', callback_data='first_step_tech')
keyboard_start.add(credit_works, technical_support)

keyboard_second = types.InlineKeyboardMarkup()
keyboard_second.add(types.InlineKeyboardButton(text='Добавить данные о новом кредите:', callback_data='credit_new'))
keyboard_second.add(types.InlineKeyboardButton(text='Рассчитать кредитный пакет в процентах', callback_data='credit_calculation'))
keyboard_second.add(types.InlineKeyboardButton(text='вернуться в предыдущее меню?', callback_data='back'))


def check_name():

    f = open('data.json', 'r')
    result = os.stat('data.json').st_size != 0   # if full

    return result

def check_credit_story():

    f = open('data_credit.json', 'r')
    result = os.stat('data_credit.json').st_size != 0   # if full

    return result

def check_tech_suppor():

    f = open('save_tech_support.json', 'r')
    result = os.stat('data_credit.json').st_size != 0   # if full

    return result

def get_name():
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    return  data["name"]


def save_name(name):
    with open('data.json', 'w') as f:
        data = {}
        data["name"] = name
        json.dump(data, f)

def save_tech_support(question):
    if check_tech_suppor()== True:
        f =  open('save_tech_support.json', 'r')
        data = json.loads(f.read())
        data ['question'].append(question)
        json.dump(data, f)
    else:
        data = {"question":[]}
        data["question"].append(question)
        f =  open('data_credit.json', 'w')
        json.dump(data, f)



def save_credit_story_bank(bank,summa):
    if check_credit_story()==True:
        f =  open('data_credit.json', 'r')
        data = json.loads(f.read())
        for i in data['bank']:
            if list(i.keys())[0]==bank:
                sum =  list(i.values())[0]+summa
                i[bank]=sum
                break
            else:
                data['bank'].append({bank:summa})
        f =  open('data_credit.json', 'w')
        json.dump(data, f)
    else:
        f =  open('data_credit.json', 'w')
        data= {}
        data['bank']=[{bank:summa}]
        json.dump(data, f)

