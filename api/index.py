import json
from http.server import BaseHTTPRequestHandler
import telebot

TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc"
bot = telebot.TeleBot(TOKEN, threaded=False)

# Автоматическая привязка вебхука при старте
try:
    webhook_url = "https://vercel.app"
    bot.set_webhook(url=webhook_url)
except Exception:
    pass

# РЕЖИМ 1: Ответ на обычные сообщения прямо боту в ЛС (на /start или старт)
@bot.message_handler(content_types=['text'])
def handle_direct_message(message):
    # Проверяем, что это личные сообщения с ботом
    if message.chat.type == "private":
        user_text = message.text.lower().strip()
        if user_text in ["/start", "старт"]:
            bot.send_message(message.chat.id, "Привет")

# РЕЖИМ 2: Ответ от твоего имени в Telegram Business (на слово "привет")
@bot.business_message_handler(content_types=['text'])
def handle_business_message(message):
    user_text = message.text.lower().strip()
    if user_text == "привет":
        bot.send_message(
            chat_id=message.chat.id, 
            text="Привет грцодыдс", 
            business_connection_id=message.business_connection_id
        )

# Обработчик запросов от Vercel
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
