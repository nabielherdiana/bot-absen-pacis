from telegram import Update, Bot
from telegram.ext import Application, Updater, CommandHandler, CallbackContext
import schedule
import time
import threading
import requests

TOKEN = "7714746694:AAF4xdrr5qnIUMJuQQcndLKW1sMA7zNn3mE"
CHAT_ID = "923124143"
bot = Bot(token=TOKEN)

updater.start_polling(drop_pending_updates=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Halo! Saya bot.")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()


# Jadwal kuliah berdasarkan gambar
jadwal_kuliah = [
    {"hari": "Minggu", "waktu": "21:08", "mata_kuliah": "Analisis Data Multivariat 2"},
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
    pesan = f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    bot.send_message(chat_id=CHAT_ID, text=pesan)

# Menjadwalkan pengingat
def atur_jadwal():
    for jadwal in jadwal_kuliah:
        waktu_kuliah = jadwal["waktu"]
        hari_kuliah = jadwal["hari"]

        # Convert hari ke format Python
        hari_dict = {
            "Senin": "monday",
            "Selasa": "tuesday",
            "Rabu": "wednesday",
            "Kamis": "thursday",
            "Jumat": "friday",
            "Sabtu": "saturday",
            "Minggu": "sunday"
        }

        # Atur pengingat 15 menit sebelum kuliah dimulai
        jam, menit = map(int, waktu_kuliah.split(":"))
        menit -= 15  # Kurangi 15 menit untuk pengingat
        if menit < 0:
            jam -= 1
            menit += 60

        waktu_notifikasi = f"{jam:02}:{menit:02}"

        schedule.every().monday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal) if hari_kuliah == "Senin" else None
        schedule.every().tuesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal) if hari_kuliah == "Selasa" else None
        schedule.every().wednesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal) if hari_kuliah == "Rabu" else None
        schedule.every().thursday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal) if hari_kuliah == "Kamis" else None
        schedule.every().friday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal) if hari_kuliah == "Jumat" else None

# Jalankan bot
if __name__ == "__main__":
    atur_jadwal()
    print("⏳ Bot pengingat kuliah berjalan...")

    while True:
        schedule.run_pending()
        time.sleep(1)

import logging

logging.basicConfig(level=logging.DEBUG)

