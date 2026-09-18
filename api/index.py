import json
from http.server import BaseHTTPRequestHandler
import telebot

TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc"
bot = telebot.TeleBot(TOKEN, threaded=False)

# Автоматически ставим правильный вебхук
try:
    bot.set_webhook(url="https://vercel.app")
except Exception:
    pass

# Режим 1: Если пишут напрямую боту в ЛС
@bot.message_handler(content_types=['text'])
def handle_direct_message(message):
    if message.chat.type == "private":
        user_text = message.text.lower().strip()
        if user_text in ["/start", "старт"]:
            bot.send_message(message.chat.id, "Привет")

# Режим 2: Если пишут тебе в личные сообщения (Telegram Business)
@bot.business_message_handler(content_types=['text'])
def handle_business_message(message):
    user_text = message.text.lower().strip()
    if user_text == "привет":
        bot.send_message(
            chat_id=message.chat.id, 
            text="Привет грцодыдс", 
            business_connection_id=message.business_connection_id
        )

# Серверная часть для Vercel
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Бизнес-бот успешно запущен и работает!".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # ИСПРАВЛЕНО: Декодируем и передаем строку, а не объект JSON
        request_body = post_data.decode('utf-8')
        
        try:
            update = telebot.types.Update.de_json(request_body)
            bot.process_new_updates([update])
        except Exception:
            pass
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'ok')
        
