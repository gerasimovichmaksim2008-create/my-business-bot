import json
from http.server import BaseHTTPRequestHandler
import telebot

TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc"
bot = telebot.TeleBot(TOKEN, threaded=False)

# Этот кусок кода САМ включит вебхук, как только сервер Vercel запустится
try:
    webhook_url = "https://vercel.app"
    bot.set_webhook(url=webhook_url)
    print("Вебхук успешно установлен автоматически!")
except Exception as e:
    print(f"Ошибка установки вебхука: {e}")

@bot.business_message_handler(content_types=['text'])
def handle_business_message(message):
    if message.text.lower().strip() == "привет":
        bot.send_message(
            chat_id=message.chat.id, 
            text="Привет грцодыдс", 
            business_connection_id=message.business_connection_id
        )

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data.decode('utf-8'))
        update = telebot.types.Update.de_json(body)
        bot.process_new_updates([update])
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'ok')
        
