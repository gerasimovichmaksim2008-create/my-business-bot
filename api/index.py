import json
import traceback
from http.server import BaseHTTPRequestHandler
import telebot

TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc"
bot = telebot.TeleBot(TOKEN, threaded=False)  # Потоки строго выключены!

# Автоматическая привязка вебхука
try:
    bot.set_webhook(url="https://vercel.app")
except Exception as e:
    print(f"[LOG] Ошибка установки вебхука: {e}")

# Режим 1: Если пишут напрямую боту в ЛС
@bot.message_handler(content_types=['text'])
def handle_direct_message(message):
    try:
        if message.chat.type == "private":
            user_text = message.text.lower().strip()
            print(f"[LOG] Получено личное сообщение: {user_text}")
            if user_text in ["/start", "старт"]:
                bot.send_message(message.chat.id, "Привет")
                print("[LOG] Ответ 'Привет' успешно отправлен в ЛС")
    except Exception as e:
        print(f"[LOG] Ошибка в message_handler: {e}")

# Режим 2: Если пишут тебе в личные сообщения (Telegram Business)
@bot.business_message_handler(content_types=['text'])
def handle_business_message(message):
    try:
        user_text = message.text.lower().strip()
        print(f"[LOG] Получено бизнес-сообщение: {user_text}")
        if user_text == "привет":
            bot.send_message(
                chat_id=message.chat.id, 
                text="Привет грцодыдс", 
                business_connection_id=message.business_connection_id
            )
            print("[LOG] Бизнес-ответ успешно отправлен")
    except Exception as e:
        print(f"[LOG] Ошибка в business_message_handler: {e}")

# Серверная часть Vercel
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Бизнес-бот успешно запущен и логирование активно!".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_body = post_data.decode('utf-8')
        
        print(f"[LOG] Входящий POST запрос от Telegram: {request_body}")
        
        try:
            update = telebot.types.Update.de_json(request_body)
            # Принудительно обрабатываем обновления до завершения функции
            bot.process_new_updates([update])
        except Exception as e:
            print(f"[LOG] Критическая ошибка парсинга: {e}")
            traceback.print_exc()
        
        # Отдаем ответ только ПОСЛЕ обработки данных бота
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'ok')
