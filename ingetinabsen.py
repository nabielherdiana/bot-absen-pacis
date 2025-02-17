import os
import logging
import time
import schedule
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Ambil token dari environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Pastikan ini diatur di Railway

# Logging untuk debugging
logging.basicConfig(level=logging.INFO)

# Jadwal kuliah berdasarkan gambar
jadwal_kuliah = [
    {"hari": "Minggu", "waktu": "21:21", "mata_kuliah": "Analisis Data Multivariat 2"},
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

async def start(update: Update, context: CallbackContext) -> None:
    """Fungsi untuk menangani perintah /start"""
    await update.message.reply_text("Halo! Saya bot pengingat kuliah Anda.")

async def kirim_notifikasi(jadwal: dict, application: Application):
    """Mengirim notifikasi pengingat kuliah"""
    pesan = (
        f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n"
        f"🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    )
    if CHAT_ID:
        await application.bot.send_message(chat_id=CHAT_ID, text=pesan)
    else:
        logging.warning("CHAT_ID belum diatur!")

def atur_jadwal(application: Application):
    """Menjadwalkan notifikasi berdasarkan jadwal kuliah"""
    hari_dict = {
        "Senin": "monday",
        "Selasa": "tuesday",
        "Rabu": "wednesday",
        "Kamis": "thursday",
        "Jumat": "friday",
        "Sabtu": "saturday",
        "Minggu": "sunday"
    }

    for jadwal in jadwal_kuliah:
        hari_kuliah = jadwal["hari"]
        waktu_kuliah = jadwal["waktu"]

        jam, menit = map(int, waktu_kuliah.split(":"))
        menit -= 15  # Kurangi 15 menit untuk pengingat
        if menit < 0:
            jam -= 1
            menit += 60

        waktu_notifikasi = f"{jam:02}:{menit:02}"

        if hari_kuliah in hari_dict:
            getattr(schedule.every(), hari_dict[hari_kuliah]).at(waktu_notifikasi).do(
                lambda: asyncio.run(kirim_notifikasi(jadwal, application))
            )

async def schedule_loop():
    """Looping untuk menjalankan schedule"""
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    """Main function untuk menjalankan bot dan scheduler"""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Menjalankan scheduler
    atur_jadwal(application)
    
    # Menjalankan bot dan scheduler secara bersamaan
    await asyncio.gather(
        application.run_polling(),
        schedule_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
