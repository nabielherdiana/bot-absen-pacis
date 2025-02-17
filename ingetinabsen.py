import logging
import time
import schedule
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# 📌 Masukkan token dan chat ID langsung di sini
TOKEN = "7714746694:AAF4xdrr5qnIUMJuQQcndLKW1sMA7zNn3mE"
CHAT_ID = "923124143"  # Ganti dengan chat ID Anda

# 🔍 Logging untuk debugging
logging.basicConfig(level=logging.INFO)

# 🗓️ Jadwal kuliah berdasarkan gambar
jadwal_kuliah = [
    {"hari": "Senin", "waktu": "18:16", "mata_kuliah": "Analisis Data Multivariat 2"},
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

# 🎯 Fungsi command /start
async def start(update: Update, context: CallbackContext) -> None:
    """Fungsi untuk menangani perintah /start"""
    await update.message.reply_text("Halo! Saya bot pengingat kuliah Anda.")

# 🔔 Fungsi untuk mengirim notifikasi pengingat kuliah
async def kirim_notifikasi(jadwal: dict, application: Application):
    """Mengirim notifikasi pengingat kuliah ke Telegram"""
    pesan = (
        f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n"
        f"🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    )
    try:
        await application.bot.send_message(chat_id=CHAT_ID, text=pesan)
        logging.info(f"📨 Notifikasi terkirim: {pesan}")
    except Exception as e:
        logging.error(f"❌ Gagal mengirim notifikasi: {e}")

# 🕒 Menjadwalkan pengingat kuliah
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

        # Mengatur notifikasi 15 menit sebelum kuliah dimulai
        jam, menit = map(int, waktu_kuliah.split(":"))
        menit -= 15
        if menit < 0:
            jam -= 1
            menit += 60

        waktu_notifikasi = f"{jam:02}:{menit:02}"

        if hari_kuliah in hari_dict:
            getattr(schedule.every(), hari_dict[hari_kuliah]).at(waktu_notifikasi).do(
                lambda: asyncio.run(kirim_notifikasi(jadwal, application))
            )

# ♻️ Looping untuk menjalankan schedule
async def schedule_loop():
    """Looping untuk menjalankan schedule secara terus-menerus"""
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# 🚀 Main function untuk menjalankan bot dan scheduler
async def main():
    """Main function untuk menjalankan bot polling dan scheduler"""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Menjalankan scheduler
    atur_jadwal(application)

    # Menjalankan bot polling dan scheduler secara bersamaan
    await asyncio.gather(
        application.run_polling(),
        schedule_loop()
    )

# 🔥 Jalankan bot
if __name__ == "__main__":
    asyncio.run(main())
