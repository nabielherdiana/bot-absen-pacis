from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = "7714746694:AAF4xdrr5qnIUMJuQQcndLKW1sMA7zNn3mE"

# Gunakan Application, bukan Updater (Telegram Bot API terbaru)
app = Application.builder().token(TOKEN).build()

# Fungsi untuk menangani /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Bot berhasil berjalan 🚀")

# Tambahkan handler
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("Bot sedang berjalan...")
    app.run_polling()
    
app.run_polling(drop_pending_updates=True)


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

