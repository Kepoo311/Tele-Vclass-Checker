import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from moodle import cek_tugas_belum_dikumpulkan, _login_only

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

SESSION_VALID = False
VCLASS_USER = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SESSION_VALID, VCLASS_USER

    if update.effective_user.id != ALLOWED_USER_ID:
        return

    await update.message.reply_text("🔐 Validasi akun VClass...")
    print("▶️ /start dipanggil")

    username = await _login_only()
    if not username:
        await update.message.reply_text("❌ Validasi gagal. Cek akun VClass.")
        return

    SESSION_VALID = True
    VCLASS_USER = username

    await update.message.reply_text(
        f"✅ Validasi berhasil\n👤 Username VClass: `{VCLASS_USER}`",
        parse_mode="Markdown"
    )
    print("✅ Session valid untuk:", VCLASS_USER)


async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    if not SESSION_VALID:
        await update.message.reply_text(
            "⚠️ Silakan jalankan /start terlebih dahulu."
        )
        return

    msg = await update.message.reply_text("⏳ Mengecek tugas...")

    async def progress(text):
        try:
            await msg.edit_text(text)
        except:
            pass

    try:
        hasil = await cek_tugas_belum_dikumpulkan(progress_cb=progress)
    except Exception as e:
        print("❌ [BOT] Error:", e)
        await msg.edit_text("❌ Terjadi error saat mengecek tugas.")
        return

    total = sum(len(v) for v in hasil.values())

    if total == 0:
        await msg.edit_text("✅ Tidak ada tugas yang belum dikumpulkan.")
        return

    pesan = "📌 *RINGKASAN TUGAS BELUM DIKUMPULKAN*\n\n"
    pesan += f"*Total:* {total} tugas\n\n"

    for course, tasks in hasil.items():
        pesan += f"📘 *{course}*\n"
        pesan += f"- {len(tasks)} tugas\n"
        for t in tasks:
            pesan += f"  • {t['judul']}\n"
            pesan += f"    🔗 {t['url']}\n"
        pesan += "\n"

    await msg.edit_text(pesan, parse_mode="Markdown")


def main():
    print("🤖 BOT PROD berjalan")
    print("🟢 Menunggu /start")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cek", cek))
    app.run_polling()


if __name__ == "__main__":
    main()
