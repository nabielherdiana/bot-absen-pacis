import asyncio
import logging
import time
import schedule
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Ganti dengan token dan chat_id Anda
TOKEN = "7714746694:AAHhr5XXE_CmVlfDChQpGwOrxJZf07lX9kg"
CHAT_ID = "923124143"

async def reset_webhook():
    bot = Bot(token=TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)  # Hapus webhook

asyncio.run(reset_webhook())  # Jalankan sekali sebelum polling

# ✅ Inisialisasi bot Telegram
bot = Bot(token=TOKEN)

# ✅ Fungsi ketika /start diketik
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("⚡️ Siap buat ngga ketinggalan absen pacis bro? 💥")

# ✅ Membuat aplikasi bot
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# ✅ Jadwal kuliah
jadwal_kuliah = [
    {"hari": "Senin", "waktu": "18:34", "mata_kuliah": "Analisis Data Multivariat 2"},
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


# ✅ Fungsi kirim notifikasi ke Telegram
def kirim_notifikasi(jadwal):
    pesan = f"⏰ Pengingat Kuliah!\n📅 Hari: {jadwal['hari']}\n🕒 Waktu: {jadwal['waktu']}\n📚 Mata Kuliah: {jadwal['mata_kuliah']}"
    bot.send_message(chat_id=CHAT_ID, text=pesan)

# ✅ Fungsi atur jadwal pengingat
def atur_jadwal():
    hari_dict = {
        "Senin": schedule.every().monday,
        "Selasa": schedule.every().tuesday,
        "Rabu": schedule.every().wednesday,
        "Kamis": schedule.every().thursday,
        "Jumat": schedule.every().friday
    }

    for jadwal in jadwal_kuliah:
        hari_kuliah = jadwal["hari"]
        waktu_kuliah = jadwal["waktu"]

        if hari_kuliah in hari_dict:
            jam, menit = map(int, waktu_kuliah.split(":"))
            menit -= 15  # Ingatkan 15 menit sebelum
            if menit < 0:
                jam -= 1
                menit += 60
            waktu_notifikasi = f"{jam:02}:{menit:02}"

            hari_dict[hari_kuliah].at(waktu_notifikasi).do(kirim_notifikasi, jadwal)

# ✅ Fungsi utama
async def main():
    atur_jadwal()
    print("⏳ Bot pengingat kuliah berjalan...")

    # ✅ Jalankan polling tanpa async loop tambahan
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # ✅ Loop untuk scheduler
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# ✅ Menjalankan program di Railway
if __name__ == "__main__":
    asyncio.run(main())  # 🚀 Pasti jalan di Railway tanpa error!
