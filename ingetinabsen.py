import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import schedule
import time

TOKEN = "7714746694:AAHhr5XXE_CmVlfDChQpGwOrxJZf07lX9kg"
CHAT_ID = "923124143"  # Ganti dengan chat ID Anda

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Saya bot Anda. Siap membantu Anda!")

# Fungsi untuk mengirim notifikasi
def kirim_notifikasi(jadwal):
    pesan = f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    application.bot.send_message(chat_id=CHAT_ID, text=pesan)

# Fungsi untuk mengatur jadwal kuliah dan pengingat
def atur_jadwal():
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
    
    for jadwal in jadwal_kuliah:
        waktu_kuliah = jadwal["waktu"]
        hari_kuliah = jadwal["hari"]

        # Mengurangi 15 menit untuk pengingat
        jam, menit = map(int, waktu_kuliah.split(":"))
        menit -= 15
        if menit < 0:
            jam -= 1
            menit += 60

        waktu_notifikasi = f"{jam:02}:{menit:02}"

        # Menambahkan notifikasi pada jadwal yang sesuai
        if hari_kuliah == "Senin":
            schedule.every().monday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif hari_kuliah == "Selasa":
            schedule.every().tuesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif hari_kuliah == "Rabu":
            schedule.every().wednesday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif hari_kuliah == "Kamis":
            schedule.every().thursday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)
        elif hari_kuliah == "Jumat":
            schedule.every().friday.at(waktu_notifikasi).do(kirim_notifikasi, jadwal)

# Fungsi utama untuk menjalankan bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Menjalankan polling untuk mendengarkan update
    await application.run_polling()

if __name__ == "__main__":
    # Menjalankan pengingat dan bot
    atur_jadwal()
    print("⏳ Bot pengingat kuliah berjalan...")

    # Menggunakan asyncio.get_event_loop() untuk menjaga event loop tetap aktif
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        print(f"Error: {e}")
