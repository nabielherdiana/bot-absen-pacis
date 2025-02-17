import logging
import time
import schedule
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime

# Ganti dengan token dan chat_id yang benar
TOKEN = "7714746694:AAHhr5XXE_CmVlfDChQpGwOrxJZf07lX9kg"
CHAT_ID = "923124143"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Daftar jadwal kuliah
jadwal_kuliah = [
    {"hari": "Senin", "waktu": "19:10", "mata_kuliah": "Analisis Data Multivariat 2"},
    {"hari": "Senin", "waktu": "10:00", "mata_kuliah": "Analisis Data Kategori"},
    {"hari": "Senin", "waktu": "13:30", "mata_kuliah": "Analisis Data Multivariat 2"},
    {"hari": "Selasa", "waktu": "07:30", "mata_kuliah": "Analisis Data Kategori"},
    {"hari": "Selasa", "waktu": "10:00", "mata_kuliah": "Desain dan Analisis Data Eksperimen 2"},
    {"hari": "Selasa", "waktu": "13:00", "mata_kuliah": "Desain dan Analisis Data Eksperimen 2"},
    {"hari": "Rabu", "waktu": "07:30", "mata_kuliah": "Riset Operasional 2"},
    {"hari": "Rabu", "waktu": "13:00", "mata_kuliah": "Teori Statistika 2"},
    {"hari": "Kamis", "waktu": "07:30", "mata_kuliah": "Analisis Data Deret Waktu 1"},
    {"hari": "Kamis", "waktu": "10:00", "mata_kuliah": "Analisis Data Deret Waktu 1"},
    {"hari": "Jumat", "waktu": "09:00", "mata_kuliah": "Perancangan dan Analisis Data Percobaan Klinis"},
    {"hari": "Jumat", "waktu": "13:00", "mata_kuliah": "Analisis Data Teks"}
]

# Fungsi untuk mengirim notifikasi ke Telegram
def kirim_notifikasi(jadwal):
    try:
        pesan = f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
        logger.info(f"Notifikasi: {pesan}")
        bot.send_message(chat_id=CHAT_ID, text=pesan)
    except Exception as e:
        logger.error(f"Error saat mengirim notifikasi: {e}")

# Fungsi untuk mengatur jadwal
def atur_jadwal():
    for jadwal in jadwal_kuliah:
        # Mengonversi waktu kuliah ke format 24 jam
        jam, menit = map(int, jadwal["waktu"].split(":"))
        # Atur pengingat 15 menit sebelum kuliah dimulai
        menit -= 15  # Kurangi 15 menit untuk pengingat
        if menit < 0:
            jam -= 1
            menit += 60

        waktu_notifikasi = f"{jam:02}:{menit:02}"

        # Menyusun jadwal berdasarkan hari kuliah
        if jadwal["hari"] == "Senin":
            schedule.every().monday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif jadwal["hari"] == "Selasa":
            schedule.every().tuesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif jadwal["hari"] == "Rabu":
            schedule.every().wednesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif jadwal["hari"] == "Kamis":
            schedule.every().thursday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif jadwal["hari"] == "Jumat":
            schedule.every().friday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)

# Fungsi untuk memulai bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Hai! Selamat datang di dunia digital!\n"
        "🤖 Saya adalah bot cerdas yang siap membantu kamu\n"
        "💬 Kirimkan pesan kapan saja, dan saya akan segera merespon!\n\n"
        "⚡️ Siap memulai petualangan? 💥"
    )

# Fungsi utama untuk menjalankan bot
async def main():
    # Buat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Atur jadwal pengingat kuliah
    atur_jadwal()

    # Jalankan polling
    logger.info("Bot sedang berjalan...")
    await application.run_polling()

# Jalankan bot dengan event loop yang benar
if __name__ == "__main__":
    import asyncio

    # Memulai aplikasi dan event loop
    if __name__ == "__main__":
    atur_jadwal()
    print("Bot pengingat kuliah berjalan...")
    
    # Menjalankan event loop tanpa menggunakan asyncio.run()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

    # Loop untuk menjalankan jadwal
    while True:
        schedule.run_pending()
        time.sleep(1)
