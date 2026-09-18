from fastapi import FastAPI, Request
import urllib.request
import urllib.parse
import json

app = FastAPI()

TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc"
URL = "https://vercel.app"

# Функция прямой HTTP отправки в Telegram
def send_tg_message(chat_id, text, business_connection_id=None):
    data = {"chat_id": chat_id, "text": text}
    if business_connection_id:
        data["business_connection_id"] = business_connection_id
        
    req_url = f"https://telegram.org{TOKEN}/sendMessage"
    req = urllib.request.Request(
        req_url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Ошибка отправки: {e}")

# GET запрос (Срабатывает при переходе по ссылке в браузере)
@app.get("/")
def read_root():
    status = "Статус:"
    try:
        # Исправлено: безопасно кодируем токен и ссылку, чтобы urllib не путал двоеточие с портом
        safe_url = urllib.parse.quote(URL, safe='')
        set_url = f"https://telegram.org{TOKEN}/setWebhook?url={safe_url}"
        
        with urllib.request.urlopen(set_url) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get("ok"):
                status += " Вебхук успешно установлен напрямую!"
            else:
                status += f" Ошибка ТГ: {res.get('description')}"
    except Exception as e:
        status += f" Ошибка соединения: {e}"
        
    return f"Бизнес-бот на FastAPI успешно запущен! {status}"

# POST запрос (Сюда Telegram шлет сообщения)
@app.post("/")
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        
        # 1. Если пишут боту напрямую в ЛС
        if "message" in body:
            message = body["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "").lower().strip()
            if text in ["/start", "старт"]:
                send_tg_message(chat_id, "Привет")
                
        # 2. Если пишут тебе в ЛС (Бизнес-автоответчик)
        elif "business_message" in body:
            b_message = body["business_message"]
            chat_id = b_message["chat"]["id"]
            text = b_message.get("text", "").lower().strip()
            connection_id = b_message.get("business_connection_id")
            if text == "привет":
                send_tg_message(chat_id, "Привет грцодыдс", business_connection_id=connection_id)
                
    except Exception as e:
        print(f"Ошибка обработки: {e}")
        
    return "ok"
    
