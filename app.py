import config

from flask import Flask, request, jsonify

from bot import bot, summary

import telebot

import mdb

from telebot.apihelper import ApiException

from multiprocessing import Pool

server = Flask(__name__,
    static_url_path='',
    static_folder='.'
)

import time

def send_notify(arr):

    for chat in arr:
        try:
            bot.send_message(chat, 'ℹ️ La base de datos se ha actualizado\n\n' + summary())
        except ApiException:
            mdb.removechat(chat)

import rmessages

def send_alert(arr):

    for chat in arr:
        try:
            bot.send_message(chat, rmessages.getMessage())
        except ApiException:
            mdb.removechat(chat)

def send_remember(arr):
    message = '''Mantenerse informado de las medidas adoptadas por las autoridades de salud del país forma parte de su obligación como ciudadano en la lucha contra la pandemia de la COVID-19. En unos minutos, justo a las 11 a.m, el Ministerio de Salud Pública de la República de Cuba comenzará su habitual Conferencia de Prensa. No deje de verla, mantenernos informados es vital para apoyar a las autoridades a erradicar este mal que nos afecta a todos.'''

    for chat in arr:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

def send_claps(arr):
    message = '''Los nuevos super héroes merecen ser reverenciados. Gracias al  personal de salud por servir de ejército activo contra esta pandemia. Salgamos todos a dar un aplauso fuerte como merecen justo a las 9 p.m'''

    for chat in arr:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

def send_updating(arr):
    message = '''ℹ️ Se está trabajando en la actualización de los datos se enviará una notificación cuando se encuentre lista la información'''

    for chat in arr:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

def send_info(arr, message):
    for chat in arr:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

@server.route('/sendinfo', methods=['POST'])
def info():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'info'
        })

    try:
        mess = data['message']
    except:
        return jsonify({
            'message': 'info'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_info, args=(chats[s*500:e],mess))

    Pool().apply_async(send_info, args=(chats[le:],mess))

    return jsonify({
        'message': 'info',
    })


@server.route('/updating', methods=['POST'])
def updating():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'alert'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_updating, args=(chats[s*500:e],))

    Pool().apply_async(send_updating, args=(chats[le:],))

    return jsonify({
        'message': 'updating',
    })

@server.route('/claps', methods=['POST'])
def claps():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'claps'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_claps, args=(chats[s*500:e],))

    Pool().apply_async(send_claps, args=(chats[le:],))

    return jsonify({
        'message': 'claps',
    })

@server.route('/remember', methods=['POST'])
def remember():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'remember'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_remember, args=(chats[s*500:e],))

    Pool().apply_async(send_remember, args=(chats[le:],))

    return jsonify({
        'message': 'remember',
    })

@server.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'alert'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_alert, args=(chats[s*500:e],))

    Pool().apply_async(send_alert, args=(chats[le:],))

    return jsonify({
        'message': 'alert',
    })

@server.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'notify'
        })

    chats = mdb.allchats()

    le = None

    for s,e in enumerate(range(500, len(chats)+500, 500)):
        le = e
        Pool().apply_async(send_notify, args=(chats[s*500:e],))

    Pool().apply_async(send_notify, args=(chats[le:],))

    return jsonify({
        'message': 'notify'
    })

@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
        )]
    )

    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.boturi + config.token)
    return "!", 200
