export default async function handler(request, response) {
  const TOKEN = "7999219744:AAF_DOZOas83SbFymc7-4K2qrYvJStPGsjc";
  const URL = "https://vercel.app";

  // 1. Если зашли через браузер (GET) — принудительно обновляем вебхук
  if (request.method === 'GET') {
    try {
      const setWebhookUrl = `https://telegram.org{TOKEN}/setWebhook?url=${URL}`;
      const res = await fetch(setWebhookUrl);
      const data = await res.json();
      
      return response.status(200).send(`Бизнес-бот на Node.js запущен! Статус вебхука: ${data.ok ? 'Успешно привязан' : data.description}`);
    } catch (error) {
      return response.status(200).send(`Ошибка привязки вебхука: ${error.message}`);
    }
  }

  // 2. Если пришло сообщение от Telegram (POST)
  if (request.method === 'POST') {
    try {
      const body = request.body;

      // Режим 1: Обычное сообщение напрямую боту в ЛС
      if (body.message) {
        const chatId = body.message.chat.id;
        const text = (body.message.text || "").toLowerCase().trim();

        if (text === '/start' || text === 'старт') {
          await fetch(`https://telegram.org{TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: "Привет" })
          });
        }
      }

      // Режим 2: Автоответчик в личном ЛС через Telegram Business
      if (body.business_message) {
        const chatId = body.business_message.chat.id;
        const text = (body.business_message.text || "").toLowerCase().trim();
        const connectionId = body.business_message.business_connection_id;

        if (text === 'привет') {
          await fetch(`https://telegram.org{TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              chat_id: chatId,
              text: "Привет грцодыдс",
              business_connection_id: connectionId
            })
          });
        }
      }
    } catch (error) {
      console.error("Ошибка обработки:", error);
    }

    // Всегда отвечаем Телеграму 200 OK, чтобы он не слал повторы
    return response.status(200).send('ok');
  }

  return response.status(405).send('Method Not Allowed');
}
