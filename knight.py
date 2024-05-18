import telebot
import pytz
import os
from flask import Flask, request
from datetime import datetime

API_TOKEN = '6374061894:AAEBsJswqUmX-Yz7Ey93-eC-pbTA--nBnQg'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

CANAL_ID = '-1001878878290'

# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Mensaje de bienvenida que se enviará al usuario al usar el comando /start
    welcome_message = "<b>Hola!, Soy un bot para enviar referencias de SyxChk, Si deseas mandar una referencia del bot digita /refe</b>",

    # Enviar el mensaje de bienvenida al usuario
    bot.send_message(message.chat.id, welcome_message, parse_mode="HTML")


@server.route("/" + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "|", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://knight321-376ef0bf7aff.herokuapp.com/' + API_TOKEN)
    return "|", 200

@bot.message_handler(commands=['refe'])
def handle_ref(message):
    if message.reply_to_message and (message.reply_to_message.photo or message.reply_to_message.animation):
        # Verificar si el usuario que ejecuta el comando es el mismo que envió la imagen
        if message.reply_to_message.from_user.id == message.from_user.id:
            if message.reply_to_message.photo:
                media = message.reply_to_message.photo[-1].file_id
            elif message.reply_to_message.animation:
                media = message.reply_to_message.animation.file_id

            user = message.from_user
            user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            user_name = f"<b>Reference By:</b> {user_mention}"
            
            # Obtener la fecha actual en la zona horaria de Colombia
            timezone_colombia = pytz.timezone('America/Bogota')
            fecha_actual_colombia = datetime.now(timezone_colombia).strftime('%d/%m/%Y')
            date_sent = f"<b>Date Send:</b> <code>{fecha_actual_colombia}</code>"

            # Verificar si el mensaje del usuario es lo suficientemente largo
            user_message = message.text[5:] if len(message.text) > 5 else "<code>None</code>"
            user_message = f"<b>User Message:{user_message}</b>"

            title = "New Reference SyxChk!"
            caption = f"<b>{title}</b>\n\n{user_name}\n{date_sent}\n{user_message}"
            
            # Añadir el botón "Buy Chk"
            keyboard = telebot.types.InlineKeyboardMarkup()
            url_button = telebot.types.InlineKeyboardButton(text="Buy Chk", url="https://t.me/Uy_07")
            keyboard.add(url_button)
            
            if message.reply_to_message.photo:
                bot.send_photo(CANAL_ID, media, caption=caption, parse_mode="HTML", reply_markup=keyboard)
            elif message.reply_to_message.animation:
                bot.send_animation(CANAL_ID, media, caption=caption, parse_mode="HTML", reply_markup=keyboard)

            bot.reply_to(message, "<b>Tu Referencia sido enviada con éxito al canal!, muchas gracias por tu apoyo.</b>", parse_mode="HTML")
            
        else:
            bot.reply_to(message, "<b>Solo puede enviar la referencia el usuario que envió la imagen o gif.</b>", parse_mode="HTML")
    elif not message.reply_to_message:
        bot.reply_to(message, "<b>Debes responder a una imagen o gif para enviarla como referencia.</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, "<b>Formato incorrecto, usa /refe (mensaje), respondiendo a la foto o gif que deseas enviar como referencias.</b>", parse_mode="HTML")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))