import config

import telebot

from telebot import types

import requests

import mdb

bot = telebot.TeleBot(config.token)

def summary():
    message = "🤒 Diagnosticados: {}\n🔬 Diagnosticados hoy: {}\n🤧 Activos: {}\n😃 Recuperados: {}\n🤩 Índice de Recuperación: {}%\n✈️ Evacuados: {}\n⚰️ Fallecidos: {}\n😵 Mortalidad: {}%\n🏥 Ingresados {}\n📆 Actualizado: {}\n\n Más Información en @covid19cubadata_bot"

    data = requests.get(config.api_url + '/summary').json()

    return message.format(
        data['Diagnosticados'],
        data['DiagnosticadosDay'],
        data['Activos'],
        data['Recuperados'],
        data['Recuperacion'],
        data['Evacuados'],
        data['Muertes'],
        data['Mortalidad'],
        data['Ingresados'],
        data['Updated'],
    )

def about():
    return '''☣️ Covid19 Cuba ☣️

https://covidcuba.swlx.info

Web de Covid19 Cuba Data:

🌐 https://covid19cubadata.github.io/
🇨🇺 http://www.cusobu.nat.cu/covid/

📲 Aplicación Movil:

Apklis: https://www.apklis.cu/application/club.postdata.covid19cuba
Github: https://github.com/covid19cuba/covid19cuba-app/releases/latest/download/app.apk

👨‍💻Bot Source Code:

https://github.com/correaleyval/covid19cuba_bot
https://github.com/correaleyval/covid19cuba_api
'''

markup = types.ReplyKeyboardMarkup(row_width=1)
    
markup.add(
    types.KeyboardButton('☢️ Resumen'),
    types.KeyboardButton('☣️ Resumen con Gráficos'),
    types.KeyboardButton('⏳ Evolución de casos por días'),
    types.KeyboardButton('📝 Datos de los Tests realizados'),
    types.KeyboardButton('🇨🇺 Casos por provincias'),
    types.KeyboardButton('🚻 Casos por Sexo'),
    types.KeyboardButton('👶🏻🧔🏽 Distribución por grupos etarios'),
    types.KeyboardButton('🦠 Modo de Contagio'),
    types.KeyboardButton('🌏 Casos por Nacionalidad (Cubanos/Extranjeros)'),
    types.KeyboardButton('🗺 Distribución por nacionalidad'),
    types.KeyboardButton('ℹ️ Acerca de')
)

def registeruser(cid, username):
    bot.send_message(
        cid,
        'Hola {}, he intentado enviar respuesta a tu solicitud pero aún no has iniciado una conversación directa conmigo, por favor envíame el comando /start por privado para poder enviarte la información solicitada. Saludos de @covid19cubadata_bot'.format(username),
    )

@bot.channel_post_handler(commands=['start'])
def channel_start(message):
    cid = message.chat.id
    mdb.savechat(cid)

    bot.send_message(
        cid, 
        'Se ha activado ☢️🇨🇺 Covid19 Cuba Bot 🇨🇺☢️ para este canal. (@covid19cubadata_bot)'
    )

@bot.message_handler(commands=['start'])
def simple_start(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    try:
        bot.send_message(
            uid,
            '☢️🇨🇺 Covid19 Cuba Bot 🇨🇺☢️\n\nHola {}, espero se encuentre bien de salud.\nSeleccione una opción del teclado para obtener información sobre el estado de Cuba con respecto al SARS-COV2 (COVID19)'.format(username),
            reply_markup=markup
        )
    except:
        registeruser(cid, username)

def start_summary(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    try:
        bot.send_message(
            uid,
            summary(),
        )
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['about'])
def about_handler(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    try:
        bot.send_message(
            uid,
            about()
        )
    except:
        registeruser(cid, username)

@bot.channel_post_handler(commands=['summary'])
def channel_summary(message):
    cid = message.chat.id
    mdb.savechat(cid)

    bot.send_message(
        cid, 
        summary()
    )

@bot.message_handler(commands=['summary'])
def send_summary(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    graph1 = requests.get(config.api_url + '/summary_graph1').content
    graph2 = requests.get(config.api_url + '/summary_graph2').content

    with open('summary1.png', 'wb') as f:
        f.write(graph1)

    with open('summary2.png', 'wb') as f:
        f.write(graph2)

    try:
        bot.send_message(
            uid,
            summary()
        )
        
        bot.send_photo(uid, open('summary1.png', 'rb'))
        bot.send_photo(uid, open('summary2.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['evolution'])
def send_evolution(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    evolution_graph = requests.get(config.api_url + '/evolution').content
    recuperados_graph = requests.get(config.api_url + '/evolution_recuperados').content
    fallecidos_graph = requests.get(config.api_url + '/evolution_fallecidos').content

    with open('evolution.png', 'wb') as f:
        f.write(evolution_graph)
    
    with open('evolution_recuperados.png', 'wb') as f:
        f.write(recuperados_graph)

    with open('evolution_fallecidos.png', 'wb') as f:
        f.write(fallecidos_graph)

    try:
        bot.send_photo(uid, open('evolution.png', 'rb'))
        bot.send_photo(uid, open('evolution_recuperados.png', 'rb'))
        bot.send_photo(uid, open('evolution_fallecidos.png', 'rb'))
    except:
        registeruser(cid, username)


@bot.message_handler(commands=['sexo'])
def send_sexo(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    sexo_graph = requests.get(config.api_url + '/sexo').content
    data = requests.get(config.api_url + '/sexo_text').json()

    with open('sexo.png', 'wb') as f:
        f.write(sexo_graph)

    texto = 'Hombres: {} | Mujeres {}'.format(data['hombres'], data['mujeres'])

    try:
        bot.send_photo(uid, open('sexo.png', 'rb'), texto)
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['modo'])
def send_modo(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    modo_graph = requests.get(config.api_url + '/modo').content

    with open('modo.png', 'wb') as f:
        f.write(modo_graph)

    try:
        bot.send_photo(uid, open('modo.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['casos_extranjeros'])
def send_casos_extranjeros(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    casos_extranjeros_graph = requests.get(config.api_url + '/casos_extranjeros').content

    with open('casos_extranjeros.png', 'wb') as f:
        f.write(casos_extranjeros_graph)

    try:
        bot.send_photo(uid, open('casos_extranjeros.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['nacionalidad'])
def send_nacionalidad(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    nacionalidad_graph = requests.get(config.api_url + '/nacionalidad').content
    data = requests.get(config.api_url + '/nacionalidad_text').json()

    with open('nacionalidad.png', 'wb') as f:
        f.write(nacionalidad_graph)

    texto = 'Cubanos: {} | Extranjeros {}'.format(data['Cubanos'], data['Extranjeros'])

    try:
        bot.send_photo(uid, open('nacionalidad.png', 'rb'), texto)
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['edad'])
def send_edad(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    edad_graph = requests.get(config.api_url + '/edad').content

    with open('edad.png', 'wb') as f:
        f.write(edad_graph)

    try:
        bot.send_photo(uid, open('edad.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['test'])
def send_test(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    test_graph = requests.get(config.api_url + '/test').content

    with open('test.png', 'wb') as f:
        f.write(test_graph)

    try:
        bot.send_photo(uid, open('test.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['provincias'])
def send_provincias(message):
    cid = message.chat.id
    uid = message.from_user.id
    username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    provincias_graph = requests.get(config.api_url + '/provincias').content
    municipios_graph = requests.get(config.api_url + '/municipios').content

    with open('provincias.png', 'wb') as f:
        f.write(provincias_graph)

    with open('municipios.png', 'wb') as f:
        f.write(municipios_graph)
    
    try:
        bot.send_photo(uid, open('provincias.png', 'rb'))
        bot.send_photo(uid, open('municipios.png', 'rb'))
    except:
        registeruser(cid, username)

@bot.message_handler(commands=['notify'])
def notify(message):
    cid = message.chat.id
    uid = message.from_user.id
    # username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)
    mid = message.message_id

    cant_users = len(mdb.allchats())

    markup = types.ReplyKeyboardMarkup(row_width=1)
    
    markup.add(
        types.KeyboardButton('☢️ Resumen'),
        types.KeyboardButton('☣️ Resumen con Gráficos'),
        types.KeyboardButton('⏳ Evolución de casos por días'),
        types.KeyboardButton('📝 Datos de los Tests realizados'),
        types.KeyboardButton('🇨🇺 Casos por provincias'),
        types.KeyboardButton('🚻 Casos por Sexo'),
        types.KeyboardButton('👶🏻🧔🏽 Distribución por grupos etarios'),
        types.KeyboardButton('🦠 Modo de Contagio'),
        types.KeyboardButton('🌏 Casos por Nacionalidad (Cubanos/Extranjeros)'),
        types.KeyboardButton('🗺 Distribución por nacionalidad'),
        types.KeyboardButton('ℹ️ Acerca de'),
    )

    try:
        bot.send_message(
            uid, 
            'CID: {} MID {} USERS {}'.format(cid, mid, cant_users),
        )
    except:
        pass

from telebot.apihelper import ApiException

def send_notifiation(cid, text):
    users = mdb.allchats()

    for uid in users:
        try:
            bot.send_message(uid, text)
        except ApiException:
            mdb.removechat(uid)

from multiprocessing import Pool

import rmessages

@bot.message_handler(content_types=['text'])
def texthandler(message):
    cid = message.chat.id
    mid = message.message_id
    # uid = message.from_user.id
    # username = '{} (@{})'.format(message.from_user.first_name, message.from_user.username)
    text = message.text

    if text == '☢️ Resumen':
        start_summary(message)
    elif text == '☣️ Resumen con Gráficos':
        send_summary(message)
    elif text == '⏳ Evolución de casos por días':
        send_evolution(message)
    elif text == '📝 Datos de los Tests realizados':
        send_test(message)
    elif text == '🚻 Casos por Sexo':
        send_sexo(message)
    elif text == '👶🏻🧔🏽 Distribución por grupos etarios':
        send_edad(message)
    elif text == '🦠 Modo de Contagio':
        send_modo(message)
    elif text == '🌏 Casos por Nacionalidad (Cubanos/Extranjeros)':
        send_nacionalidad(message)
    elif text == '🇨🇺 Casos por provincias':
        send_provincias(message)
    elif text == '🗺 Distribución por nacionalidad':
        send_casos_extranjeros(message)
    elif text == 'ℹ️ Acerca de':
        about_handler(message)
    elif '🤦‍♂️' in text:
        doc = rmessages.getDoc()
        bot.reply_to(message, doc + ' No te toques la cara sin lavarte las manos')
    elif str(cid) == str(config.gadmin):
        bot.forward_message(int(config.admin), cid, mid)
        
        #Pool().apply_async(send_notifiation, args=(cid, text))

### INLINE MODE

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        info = summary()
        r = types.InlineQueryResultArticle(
            '1',
            info,
            types.InputTextMessageContent(
                info,
                parse_mode='HTML'
            )
        )

        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


import time
import sys

def main_loop():
    bot.polling(True)
    
    while 1:
        time.sleep(3)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)