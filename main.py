import telebot
import pytz
from datetime import datetime

bot = telebot.TeleBot('6374061894:AAEBsJswqUmX-Yz7Ey93-eC-pbTA--nBnQg')

CANAL_ID = '-1001878878290'

@bot.message_handler(commands=['refe'])
def handle_ref(message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo[-1].file_id
        user_name = f"<b>Reference By: @{message.from_user.username} - @SyxChkBot</b>"
        
        # Obtener la hora actual en la zona horaria de Colombia en formato de 12 horas
        timezone_colombia = pytz.timezone('America/Bogota')
        fecha_hora_colombia = datetime.now(timezone_colombia).strftime('%I:%M %p')
        time_sent = f"<b>Time Send:</b> <code>{fecha_hora_colombia}</code>"
        
        # Verificar si el mensaje del usuario es lo suficientemente largo
        user_message = message.text[5:] if len(message.text) > 5 else ""
        user_message = f"<b>User Message: {user_message}</b>"
        
        # Añadir el botón "Buy Chk"
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Buy Chk", url="https://t.me/Uy_07")
        keyboard.add(url_button)

        caption = f"{user_name}\n{time_sent}\n{user_message}"
        bot.send_photo(CANAL_ID, photo, caption=caption, parse_mode="HTML", reply_markup=keyboard)
        bot.send_message(message.chat.id, "<b><i>Referencia enviada con éxito al canal!!!</i></b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Formato incorrecto, usa /ref (mensaje) respondiendo a una foto")

if __name__ == "__main__":
    bot.polling()