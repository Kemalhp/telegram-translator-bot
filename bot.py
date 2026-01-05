import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from deep_translator import GoogleTranslator

# 🔑 BOT TOKEN (міндетті түрде тырнақшада!)
BOT_TOKEN = "8486831996:AAHmQo5tbuYClXB_eIMuVJglFmAUm4WdRmc"

# 🔁 Пайдаланушы режимін сақтау: user_id -> "kz" | "en" | "ru"
user_mode = {}

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Қош келдіңіз!\n\n"
        "🤖 Бұл бот мәтінді аударуға арналған.\n"
        "Алдымен аудару режимін таңдаңыз, содан кейін мәтін жіберіңіз.\n\n"
        "🔹 /kz — 🇰🇿 Қазақша → 🇬🇧 Ағылшынша + 🇷🇺 Орысша\n"
        "🔹 /en — 🇬🇧 Ағылшынша → 🇰🇿 Қазақша + 🇷🇺 Орысша\n"
        "🔹 /ru — 🇷🇺 Орысша → 🇰🇿 Қазақша + 🇬🇧 Ағылшынша\n\n"
        "🔁 Режимді кез келген уақытта ауыстыруға болады.\n"
        "ℹ️ /mode — режимдер тізімі\n\n"
        "📌 Мысал:\n"
        "/en\n"
        "I want to be an engineer"
    )

# ---------- /mode ----------
async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔁 Аудару режимін ауыстыру:\n\n"
        "/kz — 🇰🇿 Қазақша → 🇬🇧 Ағылшынша + 🇷🇺 Орысша\n"
        "/en — 🇬🇧 Ағылшынша → 🇰🇿 Қазақша + 🇷🇺 Орысша\n"
        "/ru — 🇷🇺 Орысша → 🇰🇿 Қазақша + 🇬🇧 Ағылшынша\n\n"
        "Қалаған режимді таңдаңыз."
    )

# ---------- РЕЖИМ ТАҢДАУ ----------
async def set_kz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.effective_user.id] = "kz"
    await update.message.reply_text(
        "✅ Режим орнатылды:\n"
        "🇰🇿 Қазақша → 🇬🇧 Ағылшынша + 🇷🇺 Орысша\n\n"
        "Қазақша мәтін жіберіңіз.\n"
        "🔁 Басқа режим үшін /en немесе /ru жазыңыз."
    )

async def set_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.effective_user.id] = "en"
    await update.message.reply_text(
        "✅ Режим орнатылды:\n"
        "🇬🇧 Ағылшынша → 🇰🇿 Қазақша + 🇷🇺 Орысша\n\n"
        "Ағылшынша мәтін жіберіңіз.\n"
        "🔁 Басқа режим үшін /kz немесе /ru жазыңыз."
    )

async def set_ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.effective_user.id] = "ru"
    await update.message.reply_text(
        "✅ Режим орнатылды:\n"
        "🇷🇺 Орысша → 🇰🇿 Қазақша + 🇬🇧 Ағылшынша\n\n"
        "Орысша мәтін жіберіңіз.\n"
        "🔁 Басқа режим үшін /kz немесе /en жазыңыз."
    )

# ---------- АУДАРМА ----------
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    if uid not in user_mode:
        await update.message.reply_text(
            "❗ Алдымен аудару режимін таңдаңыз:\n\n"
            "/kz — Қазақша → EN + RU\n"
            "/en — Ағылшынша → KZ + RU\n"
            "/ru — Орысша → KZ + EN\n\n"
            "ℹ️ Көмек үшін /mode жазыңыз."
        )
        return

    mode_selected = user_mode[uid]

    try:
        if mode_selected == "kz":
            en = GoogleTranslator(source="kk", target="en").translate(text)
            ru = GoogleTranslator(source="kk", target="ru").translate(text)

            reply = (
                "🇰🇿 Қазақша:\n" + text + "\n\n"
                "🇬🇧 Ағылшынша:\n" + en + "\n\n"
                "🇷🇺 Орысша:\n" + ru
            )

        elif mode_selected == "en":
            kz = GoogleTranslator(source="en", target="kk").translate(text)
            ru = GoogleTranslator(source="en", target="ru").translate(text)

            reply = (
                "🇬🇧 English:\n" + text + "\n\n"
                "🇰🇿 Қазақша:\n" + kz + "\n\n"
                "🇷🇺 Орысша:\n" + ru
            )

        elif mode_selected == "ru":
            kz = GoogleTranslator(source="ru", target="kk").translate(text)
            en = GoogleTranslator(source="ru", target="en").translate(text)

            reply = (
                "🇷🇺 Русский:\n" + text + "\n\n"
                "🇰🇿 Қазақша:\n" + kz + "\n\n"
                "🇬🇧 English:\n" + en
            )

        else:
            reply = "❌ Белгісіз режим"

    except Exception:
        reply = "❌ Аударма кезінде қате пайда болды"

    await update.message.reply_text(reply)

# ---------- APP ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mode", mode))
app.add_handler(CommandHandler("kz", set_kz))
app.add_handler(CommandHandler("en", set_en))
app.add_handler(CommandHandler("ru", set_ru))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

print("Bot is running...")
app.run_polling()

