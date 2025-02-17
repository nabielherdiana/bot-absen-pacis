import asyncio
import logging
import time
import schedule
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Ganti dengan token dan chat_id Anda
TOKEN = "7714746694:AAHhr5XXE_CmVlfDChQpGwOrxJZf07lX9kg"
CHAT_ID = "923124143"

# ✅ Inisialisasi bot secara langsung
bot = Bot(token=TOKEN)

# ✅ Fungsi saat /start dipanggil
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Saya bot Anda.")

# ✅ Membuat aplikasi bot
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# ✅ Data jadwal kuliah
jadwal_kuliah = [
    {"hari": "Senin", "waktu": "18:20", "mata_kuliah": "Analisis Data Multivariat 2"},
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
# ✅ Fungsi untuk mengirim notifikasi ke Telegram
def kirim_notifikasi(jadwal):
    pesan = f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    bot.send_message(chat_id=CHAT_ID, text=pesan)

# ✅ Menjadwalkan pengingat
def atur_jadwal():
    hari_dict = {
        "Senin": "monday",
        "Selasa": "tuesday",
        "Rabu": "wednesday",
        "Kamis": "thursday",
        "Jumat": "friday"
    }

    for jadwal in jadwal_kuliah:
        hari_kuliah = jadwal["hari"]
        waktu_kuliah = jadwal["waktu"]

        if hari_kuliah in hari_dict:
            jam, menit = map(int, waktu_kuliah.split(":"))
            menit -= 15  # Atur pengingat 15 menit sebelum kuliah
            if menit < 0:
                jam -= 1
                menit += 60
            waktu_notifikasi = f"{jam:02}:{menit:02}"

            getattr(schedule.every(), hari_dict[hari_kuliah]).at(waktu_notifikasi).do(kirim_notifikasi, jadwal)

# ✅ Fungsi utama menjalankan polling dan scheduler
async def main():
    atur_jadwal()
    print("⏳ Bot pengingat kuliah berjalan...")
    
    # ✅ Menjalankan polling dalam task async
    task_polling = asyncio.create_task(application.run_polling())

    # ✅ Menjalankan scheduler dalam event loop async
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# ✅ Menjalankan program dengan penanganan event loop yang benar
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        asyncio.new_event_loop().run_until_complete(main())
