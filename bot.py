import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем ключи (лучше хранить в .env, но для теста можно прямо тут)
TELEGRAM_TOKEN = "8351386843:AAH2NouHN9kiarQo_duvmYF_A_sRwyzE33w"
OPENAI_API_KEY = "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"

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне новостную статью, и я попробую показать её нейтральный смысл + найти манипуляции.")

# Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Запрос в OpenAI
    prompt = f"""
Ты анализируешь новостную статью.
1. Сначала коротко изложи нейтральную суть текста (1-2 предложения).
2. Затем найди, какие манипуляции, эмоционально окрашенные слова, нелогичности или риторические приёмы использованы.
3. В конце сделай общий вывод: статья нейтральная или манипулятивная.
Текст статьи:
{user_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # можно заменить на gpt-4o или gpt-3.5
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
