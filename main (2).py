from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import random
import requests
from bs4 import BeautifulSoup
import re
import logging
import time
import dns.resolver
import socket
import whois
import ssl
from urllib.parse import urlparse
from gtts import gTTS
import os
from PIL import Image, ImageDraw, ImageFont
import io
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import asyncio
import re
import json
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
import json
from telegram.ext import ChatMemberHandler
from telegram.ext import CommandHandler, ContextTypes
import aiohttp
import httpx
import logging
from io import BytesIO
import socket
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
from dotenv import load_dotenv
from telegram.helpers import escape_markdown

logger = logging.getLogger(__name__)
USERS_FILE = "data_user.json"
REPLIES_FILE = "replies.json"
from telegram.helpers import escape_markdown

jadwal_kelas_8a = {
    "senin":
    escape_markdown("""
*📅 Jadwal Pelajaran Hari Senin (Kelas 8A)*

────────────────────
🕖 07.00–07.20 – Halaqoh
⏳ 07.20–07.25 – Transisi
🇬🇧 07.25–08.00 – English Habit / Baitul Lughoh
📖 08.10–08.45 – Bahasa Inggris
📖 08.45–09.20 – Bahasa Inggris
🍽 09.20–09.45 – Istirahat
🧪 09.45–10.20 – IPA
🇮🇩 10.20–10.55 – Bahasa Indonesia
🇮🇩 10.55–11.30 – Bahasa Indonesia
🕌 12.45–13.20 – Al-Qur'an
🕌 13.20–13.55 – Al-Qur'an
🇸🇦 13.55–14.30 – Bahasa Arab
────────────────────
👔: Baju putih + biru
> By HamzzH_BoT 🤖
""",
                    version=2),
    "selasa":
    escape_markdown("""
*📅 Jadwal Pelajaran Hari Selasa (Kelas 8A)*

────────────────────
🕖 07.00–07.20 – Halaqoh
⏳ 07.20–07.25 – Transisi
🇬🇧 07.25–08.00 – English Habit / Baitul Lughoh
🤸 08.10–08.45 – PJOK
🤸 08.45–09.20 – PJOK
🍽 09.20–09.45 – Istirahat
📐 09.45–10.20 – Matematika
📐 10.20–10.55 – Matematika
📐 10.55–11.30 – Matematika
🕌 12.45–13.20 – Al-Qur'an
🕌 13.20–13.55 – Al-Qur'an
🇸🇦 13.55–14.30 – Bahasa Arab
────────────────────
👔: Baju pandu jika ingin olahraga, baju hijau + celana hijau
> By HamzzH_BoT 🤖
""",
                    version=2),
    "rabu":
    escape_markdown("""
*📅 Jadwal Pelajaran Hari Rabu (Kelas 8A)*

────────────────────
🕖 07.00–07.20 – Halaqoh
⏳ 07.20–07.25 – Transisi
🇬🇧 07.25–08.00 – English Habit / Baitul Lughoh
🧪 08.10–08.45 – IPA
🧪 08.45–09.20 – IPA
🍽 09.20–09.45 – Istirahat
🇮🇩 09.45–10.20 – Bahasa Indonesia
🇮🇩 10.20–10.55 – Bahasa Indonesia
🇮🇩 10.55–11.30 – Bahasa Indonesia
🕌 12.45–13.20 – Al-Qur'an
🕌 13.20–13.55 – Al-Qur'an
📐 13.55–14.30 – Matematika
────────────────────
👔: Baju batik warna biru + celana biru
> By HamzzH_BoT 🤖
""",
                    version=2),
    "kamis":
    escape_markdown("""
*📅 Jadwal Pelajaran Hari Kamis (Kelas 8A)*

────────────────────
🕖 07.00–07.20 – Halaqoh
⏳ 07.20–07.25 – Transisi
🇬🇧 07.25–08.00 – English Habit / Baitul Lughoh
📐 08.10–08.45 – Matematika
📐 08.45–09.20 – Matematika
🍽 09.20–09.45 – Istirahat
📝 09.45–10.20 – IMLA
🎭 10.20–10.55 – SBDP / BJW / BK / PP / IPS
🎭 10.55–11.30 – SBDP / BJW / BK / PP / IPS
🕌 12.45–13.20 – Al-Qur'an
🕌 13.20–13.55 – Al-Qur'an
🇬🇧 13.55–14.30 – Bahasa Inggris
────────────────────
👔: Baju putih + celana putih
> By HamzzH_BoT 🤖
""",
                    version=2),
    "jumat":
    escape_markdown("""
*📅 Jadwal Pelajaran Hari Jumat (Kelas 8A)*

────────────────────
🕖 07.00–07.10 – Halaqoh
🧹 07.10–07.50 – Jasadiyah / Jumat Bersih
⏳ 07.50–08.00 – Transisi
🇬🇧 08.00–08.30 – PAI 2
🇬🇧 08.30–09.00 – PAI 2
🇬🇧 09.00–09.30 – Informatika
🍽 09.30–09.50 – Istirahat
💻 09.50–10.20 – Informatika
🕌 10.20–10.50 – PAI 1
🕌 10.50–11.20 – PAI 1
────────────────────
👔: Baju pramuka + celana coklat
> By HamzzH_BoT 🤖
""",
                    version=2)
}


def load_data():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_replies():
    try:
        with open(REPLIES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_replies(replies):
    with open(REPLIES_FILE, "w") as f:
        json.dump(replies, f, indent=2)


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_users(users_data):
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=2)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv("TOKEN")
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]
GAME_STATE = {}
GENIUS_ACCESS_TOKEN = "uAEf5-0mpCrHs1WgJ-QshiXvHYGNZjdOmuG3i7nWkkVPPUz8daUBF6tK30Yf-593"
# States untuk ConversationHandler
PASSWORD, COMMAND = range(2)
CORRECT_PASSWORD = "Hamzah gntg7dateK"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Yo! Bot is alive. Ketik /help buat liat list perintah.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('❌ Operation cancelled.')
    return ConversationHandler.END


async def helpall_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(
            photo="https://i.ytimg.com/vi/eXwZMAz9Vh8/maxresdefault.jpg",
            caption="📌 **__*FULL HELP MENU*__**",
            parse_mode="Markdown")

        help_text = """
**𝑭𝑹𝑬𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺:**
─────────────────
🤖 `/ai <pertanyaan>` – Tanya AI (RECOMENDED!)  
🎲 `/joke` – Dapet joke receh  
📈 `/rate <teks>` – Bot nilai teks kamu  
🔥 `/roast <nama>` – Roast nama orang  
💭 `/truth` – Pertanyaan truth  
🎯 `/dare` – Tantangan dare  
🎲 `/roll` – Lempar dadu  
🎱 `/8ball <pertanyaan>` – Tanya ke magic 8-ball  
🐱 `/cat` – Kirim foto kucing random  
❤️ `/love <nama1> <nama2>` – Cocokin cinta  
🔢 `/tebakangka` – Main tebak angka  
🗣 `/tts <kalimatmu>` – Text to speech  
🪄 `/stickerify <kata2 mu>` – Bikin stiker teks  
🎤 `/lyrics Genius <artis>:API <lagu>` – Cari lirik  
📖 `/define <kata>` – Arti kata pake AI  
💻 `/biner <teks>` – Teks ⇄ biner  
⏰ `/belajar <waktu>` – Pengingat belajar  
👤 `/user` – Info user  
🌟 `/gemini <pertanyaan>` – Tanya ke Gemini AI  
🎰 `/gacha` – Gacha gratis, dapat point random  
🌅 `.s` – Membuat stiker dari foto  
💻 `/dev` – Info tentang developer bot
📰 `/news` - Berita CNBC hari ini.

**𝑷𝑶𝑰𝑵𝑻 𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺**
─────────────────
🌐 `/portscan <ip>` - Scan port IP (20 ⚡️ )
🔍 `/scrape <url>` – Scrape website (10 ⚡️)
📨 `/replay <trigger> <reply>` – Auto-reply baru (5 ⚡️)k akun IG (2 ⚡️)
🧩 `/qc <kalimat>` – Bikin stiker bubble chat WhatsApp (4 ⚡️)
📸 `/igstalk <username>` - Stalk akun IG (2 ⚡️)

✨ *Have fun!*
"""
        await update.message.reply_text(help_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"[helpall_command] Error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


# /joke
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = [
        "Kenapa programmer nggak pernah kesepian? Karena selalu ada bug yang nemenin.",
        "Apa bedanya kamu sama server? Server down kadang up lagi, kamu? Nggak naik-naik.",
        "Kenapa orang ngoding nggak pernah kurus? Karena selalu ada snack bar.",
        "Kenapa laptop suka kedinginan? Karena sering buka Windows.",
        "Kenapa website jomblo? Karena gagal koneksi.",
        "Kenapa chat kamu kayak website lama? Loading-nya lama banget.",
        "Kenapa hacker susah tidur? Kebanyakan mikirin password orang.",
        "Kenapa wifi kayak mantan? Deket doang, tapi nggak nyambung.",
        "Kenapa error mirip kamu? Munculnya selalu bikin kesel.",
        "Kenapa programmer susah move on? Karena selalu stuck di loop.",
        "Kenapa mouse selalu setia? Karena selalu ikut kemana pun kita gerak.",
        "Kenapa Java dan JavaScript nggak cocok? Karena mereka cuma mirip nama.",
        "Kenapa PC suka ngambek? Karena kebanyakan beban kerja.",
        "Kenapa kamu kayak bug? Semua orang pengen hapus.",
        "Kenapa programmer suka kopi? Karena depresi sama deadline.",
        "Kenapa cloud kayak cinta? Ada, tapi nggak kelihatan.",
        "Kenapa baterai cepat habis? Karena capek liat kelakuanmu.",
        "Kenapa chat kamu kayak file zip? Harus diekstrak dulu baru paham maksudnya.",
        "Kenapa coding mirip cinta? Kalau salah satu huruf aja, hasilnya error.",
        "Kenapa mantan kayak file sampah? Harus dihapus biar lega.",
        "Kenapa dia nggak bales chat? Mungkin dia crash kayak app bajakan.",
        "Kenapa harddisk kayak kenangan? Susah diformat total.",
        "Kenapa router kayak ibu kos? Marah kalau banyak yang numpang.",
        "Kenapa username kamu rejected? Karena nggak ada yang mau terima.",
        "Kenapa kamu kayak file hidden? Disembunyiin orang biar nggak keliatan.",
        "Kenapa printer mirip kamu? Sering macet pas dibutuhin.",
        "Kenapa humor kamu kayak RAM 2GB? Nggak kuat bikin orang ketawa.",
        "Kenapa love life kamu kayak sistem trial? Berakhir sebelum sempat serius.",
        "Kenapa icon recycle bin kayak kamu? Selalu ada tapi nggak penting.",
        "Kenapa suaramu kayak fan laptop? Berisik tapi nggak ada gunanya.",
        "Kenapa OS kamu kayak mantan? Sering minta update tapi isinya gitu-gitu aja.",
        "Kenapa kamu kayak shortcut rusak? Nggak ada fungsinya.",
        "Kenapa wifi cuma satu bar? Karena sinyal perasaanmu juga lemah.",
        "Kenapa keyboard suka capek? Karena terus neken perasaan.",
        "Kenapa kamu kayak loading screen? Bikin orang nunggu tapi zonk.",
        "Kenapa powerbank kayak teman palsu? Sering ngilang pas dibutuhin.",
        "Kenapa coding kayak jatuh cinta? Sama-sama bikin stres.",
        "Kenapa chat kamu kayak spam? Nggak penting tapi selalu ada.",
        "Kenapa pacaran kayak beta version? Banyak bug dan drama.",
        "Kenapa mantan kayak cache? Harus dibersihin biar nggak ngelag.",
        "Kenapa internet kayak mood? Kadang cepat, kadang lemot nggak jelas.",
        "Kenapa hp suka drop? Karena sering jatuh sama rayuanmu.",
        "Kenapa dia nggak balas? Mungkin sinyal sayangnya ke kamu lemah.",
        "Kenapa chat kamu kayak HTML? Banyak tag tapi kosong isinya.",
        "Kenapa cinta kamu kayak wifi publik? Semua orang pernah nyoba.",
        "Kenapa dia cuma ngetik doang? Mungkin dia stuck di buffering perasaan.",
        "Kenapa kamu kayak bug? Nggak penting tapi nyebelin.",
        "Kenapa modem kayak perasaan? Kalau ditekan malah disconnect.",
        "Kenapa dia ghosting? Mungkin dia update ke versi yang lebih baru.",
        "Kenapa kamu kayak low battery? Selalu bikin orang panik.",
        "Kenapa pacaran kayak download file besar? Lama, dan sering gagal.",
        "Kenapa mantan kayak log error? Sering kebaca walau nggak mau.",
        "Kenapa file corrupt kayak kamu? Susah dipahami dan bikin ribet.",
        "Kenapa PC suka restart sendiri? Karena capek sama kamu.",
        "Kenapa dia nggak bales? Mungkin notif kamu udah dia mute.",
        "Kenapa suka coding malam? Karena kalau pagi harus pura-pura waras.",
        "Kenapa HP sering drop? Karena sering jatuh hati juga.",
        "Kenapa cinta kayak trial? Berakhir sebelum siap dibayar mahal.",
        "Kenapa kamu kayak page not found? Dicariin tapi nggak ada.",
        "Kenapa dia baca doang? Mungkin dia crash liat chat kamu.",
        "Kenapa kamu kayak plugin error? Nyebelin dan nggak kepake.",
        "Kenapa status kamu kayak server down? Semua orang nungguin balik.",
        "Kenapa mood kamu kayak update gagal? Bikin kesel semua orang.",
        "Kenapa chat kamu kayak softcase transparan? Nggak ada isinya.",
        "Kenapa kamu kayak virus? Nyebarinnya bikin orang kesel.",
        "Kenapa dia nggak read? Mungkin sinyal hatinya hilang.",
        "Kenapa wifi suka disconnect? Karena capek sama device murahan.",
        "Kenapa kamu kayak RAM penuh? Bikin semua orang lemot.",
        "Kenapa humor kamu kayak folder kosong? Nggak ada isinya.",
        "Kenapa dia nggak suka? Mungkin dia update selera.",
        "Kenapa cinta kamu kayak CPU panas? Nggak sehat lama-lama.",
        "Kenapa kamu kayak driver error? Susah nyambung sama siapa pun.",
        "Kenapa password cinta kamu lemah? Karena semua orang bisa nebak.",
        "Kenapa dia read doang? Mungkin dia lagi uninstall rasa.",
        "Kenapa kamu kayak file duplicate? Sama-sama nggak penting.",
        "Kenapa humor kamu kayak VGA jadul? Nggak ada yang ketawa liatnya.",
        "Kenapa dia nggak jawab? Mungkin crash kena bug cinta.",
        "Kenapa dia typing lama? Mungkin sinyal sayangnya buffering.",
        "Kenapa mantan kayak recycle bin? Harus dikosongin biar lega.",
        "Kenapa kamu kayak pop-up iklan? Tiba-tiba muncul bikin bete.",
        "Kenapa HP lowbat? Karena sering nyari perhatian kamu.",
        "Kenapa dia read doang? Mungkin dia uninstall chat kamu.",
        "Kenapa kamu kayak demo gratis? Semua orang nyoba, nggak ada yang beli.",
        "Kenapa humor kamu kayak driver out of date? Nggak jalan sama siapa pun.",
        "Kenapa dia left group? Mungkin dia join grup lain yang lebih rame.",
        "Kenapa kamu kayak cache penuh? Bikin device orang lemot.",
        "Kenapa dia cuma view story? Mungkin dia lagi survey harga hati.",
        "Kenapa cinta kamu kayak softcase bening? Nggak ada yang notice.",
        "Kenapa dia ghosting? Mungkin dia upgrade spek target.",
        "Kenapa kamu kayak trial expired? Udah gratisan, masih nyusahin.",
        "Kenapa dia mute notif kamu? Mungkin suaramu bikin ilfeel.",
        "Kenapa humor kamu kayak iklan 5 detik? Nggak ada yang mau nonton.",
        "Kenapa kamu kayak share location? Semua orang bisa liat, nggak ada yang dateng.",
        "Kenapa dia nggak reply? Mungkin dia restart device hati.",
        "Kenapa humor kamu kayak site maintenance? Nggak aktif lama-lama.",
        "Kenapa kamu kayak template power point? Semua orang punya, nggak ada yang spesial.",
        "Kenapa dia typing doang? Mungkin crash kena bug chat.",
        "Kenapa humor kamu kayak RAM jadul? Gagal bikin ketawa.",
        "Kenapa kamu kayak file temp? Harus dihapus biar lega.",
        "Kenapa dia left? Mungkin join server lain yang lebih seru.",
        "Kenapa humor kamu kayak loader 1%? Lama dan nggak ngaruh.",
        "Kenapa cinta kamu kayak WiFi publik? Semua orang pernah coba."
    ]
    await update.message.reply_text(random.choice(jokes))


# /rate
async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        teks = " ".join(context.args)
        nilai = random.randint(1, 100)
        await update.message.reply_text(f"Nilai untuk '{teks}': {nilai}/100")
    else:
        await update.message.reply_text("Contoh: /rate Python")


# /roast
async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        target = " ".join(context.args)
        roasts = [
            f"{target}, muka kamu kayak bug yang susah di-fix.",
            f"{target}, IQ kamu kayak sinyal WiFi... putus nyambung.",
            f"{target}, sabar ya... tampan nggak, kaya juga nggak.",
            f"{target}, kayak komentar spam, nggak penting tapi tetap muncul.",
            f"{target}, otakmu loading lebih lama dari Windows XP.",
            f"{target}, ngeliat kamu kayak error 404: personality not found.",
            f"{target}, suaramu cocoknya jadi alarm biar orang cepet bangun.",
            f"{target}, bercanda sama kamu kayak main game lag parah, nggak ada senengnya.",
            f"{target}, kayak password default, gampang ditebak dan nggak penting.",
            f"{target}, kalo kamu jadi karakter game, pasti NPC paling useless.",
            f"{target}, wajah kamu cocok jadi watermark, transparan aja sekalian.",
            f"{target}, pinter banget... pinter bikin kesel orang.",
            f"{target}, kayak iklan Youtube, nggak ada yang mau liat.",
            f"{target}, kalo ada lomba nyebelin, kamu juara bertahan.",
            f"{target}, humormu tuh kayak Java update, basi dan bikin kesel.",
            f"{target}, bercanda sama kamu kayak disk penuh, nggak ada space buat ketawa.",
            f"{target}, coba kamu diem, mungkin ada yang jadi suka.",
            f"{target}, ngomong sama kamu bikin otak pingin uninstall sendiri.",
            f"{target}, kayak sinyal EDGE, bikin emosi terus.",
            f"{target}, kalau ada diskon attitude, kamu tetap nggak kebeli.",
            f"{target}, wajah kamu kayak captcha, bikin orang males login.",
            f"{target}, denger pendapat kamu kayak baca terms & conditions, skip aja.",
            f"{target}, bercanda sama kamu kayak stuck di loading screen.",
            f"{target}, mukamu cocok jadi logo 'Try Again'.",
            f"{target}, kayak printer jadul, berisik tapi nggak kepake.",
            f"{target}, lucumu kayak update Windows, datangnya nggak diundang.",
            f"{target}, otakmu buffering sejak lahir ya?",
            f"{target}, kayak spoiler film, semua orang pengen jauhin.",
            f"{target}, muka kamu kayak hidden folder, mending nggak usah dibuka.",
            f"{target}, ketawamu kayak iklan pop-up, muncul tiba-tiba bikin ilfeel.",
            f"{target}, kayak charger KW, bikin rusak suasana.",
            f"{target}, wajah kamu kayak low resolution, burem masa depan juga.",
            f"{target}, suaranya kayak ringtone jadul, bikin sakit kuping.",
            f"{target}, kalo ada upgrade otak, tolong install secepatnya ya.",
            f"{target}, kayak spam email, nggak penting tapi tetep ada.",
            f"{target}, ngeliat kamu kayak lihat jam rusak, nggak ada gunanya.",
            f"{target}, kayak history browser, semua orang pengen hapus.",
            f"{target}, mukamu kayak bug report, munculnya bikin kesel.",
            f"{target}, kalau ada update attitude, kamu skip ya?",
            f"{target}, humormu kayak video buffering, bikin males nonton.",
            f"{target}, kamu kayak foto blur, bikin sakit mata.",
            f"{target}, pinter banget… pinter bikin suasana jadi awkward.",
            f"{target}, ngomong sama kamu kayak nonton TV rusak, tetep nggak seru.",
            f"{target}, kayak pop-up iklan, bikin orang pengen close tab.",
            f"{target}, mukamu kayak expired date, nggak ada yang mau nyentuh.",
            f"{target}, kalo nyebelin jadi seni, kamu masterpiece.",
            f"{target}, ngomong sama kamu kayak nunggu loading 1%, nggak nyampe-nyampe.",
            f"{target}, wajahmu kayak fitur beta, masih banyak bug.",
            f"{target}, suaranya kayak speaker pecah, bikin pusing.",
            f"{target}, ngakak? Sama kamu? Mending ngakak ke meme basi deh.",
            f"{target}, kayak update aplikasi, orang skip kalo bisa.",
            f"{target}, bercanda sama kamu kayak buka website kena malware.",
            f"{target}, kamu kayak demo game, seru di awal, jelek di akhir.",
            f"{target}, mukamu cocok jadi icon recycle bin.",
            f"{target}, kayak sinyal satu bar, ada tapi useless.",
            f"{target}, ngeliat kamu bikin ping mental langsung naik 999+.",
            f"{target}, ketawamu kayak echo mic murah, ganggu banget.",
            f"{target}, kamu kayak login form, selalu bikin orang males ngisi.",
            f"{target}, wajah kamu kayak test pattern TV, warnanya ngaco semua.",
            f"{target}, humormu kayak lampu mati, gelap total.",
            f"{target}, kayak beta tester gagal, bug everywhere.",
            f"{target}, ngomong sama kamu kayak nunggu unduhan 99% stuck.",
            f"{target}, mukamu kayak hidden feature, nggak perlu dicari juga.",
            f"{target}, pinter? Mungkin di dunia lain.",
            f"{target}, kayak shortcut corrupt, nggak bisa dibuka.",
            f"{target}, ketawamu kayak alarm error, bikin panik doang.",
            f"{target}, ngeliat kamu kayak disk cleanup, bikin orang males.",
            f"{target}, mukamu kayak broken link, nggak ada yang mau klik.",
            f"{target}, kamu kayak OS bajakan, rawan kena virus.",
            f"{target}, bercanda sama kamu kayak modem dial-up, lemot dan nyebelin.",
            f"{target}, wajah kamu kayak draft chat, mending nggak dikirim.",
            f"{target}, kamu kayak crash report, munculnya bikin bete.",
            f"{target}, suaranya kayak speaker rusak, nyakitin telinga.",
            f"{target}, ngomong sama kamu kayak loading screen game 2005.",
            f"{target}, humormu kayak RAM 512MB, nggak kuat apa-apa.",
            f"{target}, mukamu kayak watermark gratis, ganggu pemandangan.",
            f"{target}, kayak plugin error, bikin website nggak kepake.",
            f"{target}, pinter banget… pinter bikin orang pindah server.",
            f"{target}, ngeliat kamu kayak expired domain, nggak ada fungsinya.",
            f"{target}, kamu kayak file .tmp, nggak penting dan numpuk doang.",
            f"{target}, mukamu kayak aplikasi crash, bikin restart mood orang.",
            f"{target}, ketawamu kayak ringtone Nokia polifonik, outdated.",
            f"{target}, humormu kayak meme jadul, basi dan kering.",
            f"{target}, ngomong sama kamu kayak WiFi limited, nyambung tapi nggak ada internet.",
            f"{target}, mukamu kayak iklan gratis, munculnya nyebelin.",
            f"{target}, kamu kayak captcha susah, bikin orang males lanjut.",
            f"{target}, pinter? Lebih mirip hidden feature yang nggak pernah dipake.",
            f"{target}, ngeliat kamu kayak folder kosong, useless.",
            f"{target}, suaranya kayak mic murahan, ngerecokin doang.",
            f"{target}, mukamu kayak foto low res, nggak enak diliat.",
            f"{target}, kamu kayak update 0 byte, nggak ngaruh sama sekali.",
            f"{target}, humormu kayak pop-up survey, nggak ada yang mau klik.",
            f"{target}, ngomong sama kamu kayak waiting room server full.",
            f"{target}, ketawamu kayak alarm jam 3 pagi, bikin kesel.",
            f"{target}, kamu tuh kayak bug fix yang nggak nge-fix apa pun.",
            f"{target}, mukamu kayak file corrupt, nggak bisa dibuka.",
            f"{target}, pinter? Lebih kayak typo yang nggak pernah dibenerin.",
            f"{target}, ngeliat kamu kayak buffering 0%, nggak jalan-jalan.",
            f"{target}, kamu kayak game beta broken, lebih banyak error daripada mainnya.",
            f"{target}, humormu kayak server down, bikin semua orang left."
        ]
        await update.message.reply_text(random.choice(roasts))
    else:
        await update.message.reply_text("Contoh: /roast Hamzah")


# /truth
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    truths = [
        "Siapa orang terakhir yang kamu stalk di Instagram?",
        "Pernah suka sama pacar temen sendiri?",
        "Siapa nama mantan yang masih suka kamu inget?",
        "Pernah bohong besar ke orang tua? Apa itu?",
        "Kapan terakhir kamu nangis? Kenapa?",
        "Siapa orang yang bikin kamu paling kesel saat ini?",
        "Pernah nyuri barang waktu kecil? Barang apa?",
        "Siapa gebetan pertama kamu?", "Kalau disuruh milih, cinta atau uang?",
        "Pernah suka sama guru atau dosen?",
        "Pernah pura-pura sakit biar nggak sekolah?",
        "Siapa teman yang paling kamu percaya rahasianya?",
        "Pernah jatuh cinta sama sahabat sendiri?",
        "Siapa yang paling sering kamu chat sekarang?",
        "Pernah mimpiin siapa terakhir kali?",
        "Hal paling memalukan yang pernah kamu lakuin?",
        "Pernah ghosting orang? Siapa?", "Kamu pernah diselingkuhin?",
        "Pernah selingkuh? Jujur!",
        "Siapa orang yang paling sering kamu kepoin?",
        "Pernah jatuh cinta pada pandangan pertama?",
        "Kalau bisa balikan sama mantan, mau nggak?",
        "Siapa nama mantan yang pengen kamu lupakan?",
        "Hal paling childish yang masih kamu lakuin?",
        "Pernah pura-pura nggak suka padahal suka?",
        "Kalau sekarang punya kesempatan nembak gebetan, mau nggak?",
        "Pernah bilang 'aku cinta kamu' cuma buat basa-basi?",
        "Pernah punya pikiran buat nyerahin semua?",
        "Siapa orang yang paling sering muncul di mimpi kamu?",
        "Siapa nama kontak teraneh di HP kamu?",
        "Pernah suka sama orang tapi nggak pernah bilang?",
        "Hal paling romantis yang pernah kamu lakuin?",
        "Apa ketakutan terbesar kamu?",
        "Siapa yang terakhir kali bikin kamu senyum?",
        "Pernah nangis gara-gara film? Film apa?",
        "Hal paling kamu banggakan dari diri sendiri?",
        "Pernah ngerasa nggak cukup baik buat seseorang?",
        "Siapa yang paling sering kamu pikirin sebelum tidur?",
        "Pernah jatuh cinta diam-diam? Sama siapa?",
        "Pernah ketahuan bohong? Soal apa?",
        "Pernah suka sama teman satu kelas? Siapa?",
        "Pernah bilang sayang tapi nggak beneran sayang?",
        "Apa penyesalan terbesar kamu?",
        "Pernah bilang ke orang tua 'aku benci kalian'?",
        "Siapa orang yang pertama kamu cari kalau ada masalah?",
        "Hal paling aneh yang kamu takutkan?",
        "Siapa mantan yang paling bikin kamu susah move on?",
        "Kalau sekarang ada yang nembak kamu, kamu terima nggak?",
        "Pernah ngintip chat orang? Siapa?",
        "Siapa nama teman lawan jenis yang paling dekat sama kamu?",
        "Pernah punya fake account? Buat apa?",
        "Hal paling gila yang pengen kamu coba?",
        "Apa yang paling kamu takutin di masa depan?",
        "Pernah jatuh cinta cuma karena fisik?",
        "Siapa nama pertama yang muncul di kepala kamu sekarang?",
        "Pernah diremehkan orang? Gimana rasanya?",
        "Kalau bisa ngulang waktu, kamu mau ngulang kapan?",
        "Siapa yang kamu harap balas chat kamu sekarang juga?",
        "Pernah malu banget sampe pengen ngilang? Kenapa?",
        "Pernah naksir orang lebih tua jauh? Berapa tahun bedanya?",
        "Pernah suka sama orang dari media sosial doang?",
        "Siapa yang paling sering bikin kamu marah?",
        "Pernah pacaran LDR? Gimana rasanya?",
        "Pernah ngelakuin hal bodoh demi cinta? Apa?",
        "Pernah dighosting? Sama siapa?",
        "Hal paling kamu sesali tentang mantan?",
        "Pernah kepikiran balikan sama mantan?",
        "Siapa yang kamu rinduin saat ini?", "Hal paling bikin kamu insecure?",
        "Pernah ketahuan bohong sama pacar? Soal apa?",
        "Pernah pura-pura nggak peduli padahal peduli banget?",
        "Siapa orang yang kamu harap selalu ada buat kamu?",
        "Hal paling aneh yang kamu suka?",
        "Siapa yang kamu anggap soulmate kamu?",
        "Apa kebohongan terbesar yang pernah kamu buat?",
        "Pernah suka sama dua orang sekaligus?",
        "Apa hal paling romantis yang kamu harap orang lain lakuin ke kamu?",
        "Siapa yang terakhir kali bikin kamu kecewa?",
        "Pernah nangis gara-gara cinta?",
        "Hal kecil yang bisa bikin kamu bahagia?",
        "Siapa nama teman yang paling kamu percaya rahasianya?",
        "Pernah kepikiran ninggalin semuanya dan kabur? Kenapa?",
        "Siapa yang pertama kali kamu chat setiap pagi?",
        "Pernah jatuh cinta sama orang yang udah punya pacar?",
        "Apa sifat terburuk kamu menurut kamu sendiri?",
        "Hal apa yang paling bikin kamu takut kehilangannya?",
        "Siapa yang paling sering kamu stalking story-nya?",
        "Pernah nyimpen perasaan sendiri lama banget? Berapa lama?",
        "Hal apa yang paling kamu pengen bilang ke gebetan tapi nggak berani?",
        "Siapa yang paling kamu takutin kalau dia pergi?",
        "Pernah pura-pura bahagia padahal nggak?",
        "Apa arti cinta menurut kamu?", "Pernah ngerasa nggak layak dicintai?",
        "Pernah ngerasa sayang banget sampe takut kehilangan?",
        "Kalau punya satu permintaan yang pasti dikabulin, apa?",
        "Siapa orang yang paling berharga buat kamu?",
        "Hal apa yang kamu sesali dari masa lalu?",
        "Pernah nggak bisa tidur gara-gara mikirin seseorang?",
        "Apa rahasia terbesar yang belum pernah kamu bilang ke siapa pun?"
    ]
    await update.message.reply_text(random.choice(truths))


# /dare
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dares = [
        "Chat mantan: 'Aku masih sayang'.", "Post foto jelek di story.",
        "Nyanyi keras-keras selama 10 detik.",
        "Screenshot chat terakhir dengan gebetan dan kirim ke grup.",
        "Ganti foto profil jadi foto jelek selama 1 hari.",
        "Teriak 'Aku ganteng!' atau 'Aku cantik!' 3 kali.",
        "Chat orang random: 'Kamu lucu juga ya'.",
        "Upload video nyanyi lagu anak-anak.",
        "Rekam suara bilang 'Aku suka kamu' lalu kirim ke grup.",
        "Bilang ke teman terdekat kalau kamu kangen dia.",
        "Tulis status galau di story.",
        "Tanya mantan: 'Kamu masih inget aku nggak?'.",
        "Chat gebetan: 'Kamu makan apa hari ini?'.",
        "Bikin story ngaku lagi jatuh cinta.",
        "Pura-pura marah ke teman tanpa alasan.",
        "Ngedance 10 detik dan kirim videonya.",
        "Selfie dengan ekspresi paling aneh.",
        "Bilang 'Aku jelek' di voice note lalu kirim ke grup.",
        "Chat teman lama: 'Kamu kangen aku nggak?'.",
        "Nyanyiin lagu paling kamu benci.",
        "Ganti nama kontak gebetan jadi 'Suamiku/Istriku'.",
        "Tanya ke orang random: 'Kamu single?'.",
        "Kirim emot ❤️ ke orang yang terakhir chat kamu.",
        "Ketik 'Aku sayang kamu' dan kirim ke grup keluarga.",
        "Bilang 'Aku lapar' ke orang random di DM.",
        "Pake filter jelek dan upload ke story.",
        "Tulis nama mantan di tangan, foto dan kirim ke grup.",
        "Chat guru/dosen: 'Selamat pagi, semoga sehat selalu!'.",
        "Kirim foto kaki kamu ke grup.",
        "Tulis kata pertama yg muncul di pikiranmu sekarang di story.",
        "Cerita hal memalukan yg pernah kamu alami di grup.",
        "Pura-pura nangis di voice note dan kirim.",
        "Nyanyi lagu dangdut keras-keras dan rekam.",
        "Ketik 'Aku cinta kamu' ke teman lawan jenis pertama di chat.",
        "Bilang ke sahabat: 'Aku benci kamu' lalu jelasin itu dare.",
        "Ganti bio jadi 'Aku cari jodoh'.", "Pakai baju kebalik 1 jam.",
        "Chat mantan pacar: 'Gimana kabarmu?'.",
        "Kirim sticker random ke atasan atau guru.",
        "Chat 'Aku rindu kamu' ke orang yg baru kamu kenal.",
        "Post foto random di galeri ke story.",
        "Telfon teman dan langsung bilang 'Aku kangen'.",
        "Cerita cinta pertama kamu di grup.",
        "Rekam suara bilang 'Aku malu' 5x.", "Upload foto masa kecil kamu.",
        "Ganti status jadi 'Aku butuh perhatian'.",
        "Chat 'I miss you' ke orang yang nggak deket sama kamu.",
        "Tanya ke teman: 'Kamu cinta aku nggak?'.",
        "Tulis kata 'LOVE' di kertas dan foto.",
        "Bilang 'Kamu cantik/ganteng' ke lawan jenis random.",
        "Upload selfie tanpa filter.", "Buat puisi 2 baris dan kirim ke grup.",
        "Ketik 'Aku kangen mantanku' di status.",
        "Chat orang random: 'Mau jadi temen aku?'.",
        "Tanya gebetan: 'Kalau aku nembak, diterima nggak?'.",
        "Tanya mantan: 'Kamu masih benci aku?'.",
        "Voice note ketawa 5 detik ke grup.",
        "Chat ke 3 kontak pertama: 'Aku suka kamu'.",
        "Tulis nama gebetan di story.", "Telfon teman dan langsung nyanyi.",
        "Ketik 'Aku bodoh' dan kirim ke grup.",
        "Upload quotes galau di story.",
        "Bilang 'Aku pengen punya pacar' ke sahabat lawan jenis.",
        "Pakai foto profil kartun jelek.",
        "Tulis status: 'Ada yg kangen aku nggak?'.",
        "Chat 'Kamu lagi apa?' ke orang yg jarang kamu chat.",
        "Cerita first kiss kamu di grup.", "Post emot 😍 doang di story.",
        "Tanya teman: 'Aku cantik/ganteng nggak?'.",
        "Upload foto kaki atau tangan doang.", "Kirim emot ❤️ ke mantan.",
        "Tanya ke random orang: 'Boleh kenalan?'.",
        "Chat ke 5 orang random: 'Hi!'.",
        "Bilang 'Aku sayang kamu' ke cermin dan rekam.",
        "Post story sambil tutup mata.",
        "Chat sahabat: 'Aku mau ngaku sesuatu'.",
        "Nyanyi sambil cubit pipi sendiri, kirim video.",
        "Post meme paling receh di story.",
        "Chat mantan: 'Pernah kangen aku nggak?'.",
        "Tanya orang random: 'Menurut kamu aku ganteng/cantik?'.",
        "Bilang 'I love you' ke diri sendiri dan rekam.",
        "Upload voice note bilang 'Aku malu banget'.",
        "Bilang 'Aku butuh pelukan' di story.",
        "Ketik 'Aku galau' dan kirim ke grup keluarga.",
        "Upload foto random dari galeri tanpa edit.",
        "Tanya gebetan: 'Kamu udah makan?'.",
        "Ganti bio jadi 'Jomblo cari cinta'.", "Chat mantan: 'Kangen ga?'.",
        "Voice note bilang 'Aku gemes' 3x.",
        "Upload foto makanan jelek ke story.",
        "Chat 'Aku suka kamu' ke teman lama.",
        "Tanya sahabat: 'Kalau aku nembak kamu, kamu terima nggak?'.",
        "Post story: 'Ada yg mau nemenin aku?'.",
        "Nyanyi lagu cinta sambil merem dan rekam.",
        "Tulis kata 'LOVE' di jidat dan foto.",
        "Ketik 'Aku rindu' dan kirim ke random orang.",
        "Tanya gebetan: 'Kamu suka cowok/cewek kayak aku nggak?'.",
        "Chat random: 'Kamu lucu juga ya'.",
        "Upload foto paling lawas di HP ke story.",
        "Bilang 'Aku baper' di voice note dan kirim ke grup.",
        "Chat mantan: 'Aku dulu sayang banget sama kamu'.",
        "Post emot 🥰 doang di story.", "Tanya random: 'Kamu punya pacar?'."
    ]
    await update.message.reply_text(random.choice(dares))


# /roll
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hasil = random.randint(1, 6)
    await update.message.reply_text(f"Kamu dapet: 🎲 {hasil}")


# /8ball
async def eight_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        responses = [
            "Yes", "No", "Maybe", "Definitely", "Ask again later", "Of course",
            "Never"
        ]
        await update.message.reply_text(random.choice(responses))
    else:
        await update.message.reply_text("Contoh: /8ball Apakah dia suka aku?")


# /cat
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cats = [
        "https://site-547756.mozfiles.com/files/547756/medium/catoutside.jpeg",
        "https://wallpapers.com/images/hd/cute-cat-eyes-profile-picture-uq3edzmg1guze2hh.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg",
        "https://images2.alphacoders.com/716/71660.jpg",
        "http://www.homelesstohousecats.com/wp-content/uploads/2014/10/cat-401124_1920.jpg",
        "https://cataas.com/cat", "https://cataas.com/cat/cute",
        "https://cataas.com/cat/says/Meow",
        "https://cataas.com/cat/says/Hello", "https://cataas.com/cat/says/Hi",
        "https://cataas.com/cat/says/Love",
        "https://cataas.com/cat/says/Happy",
        "https://cataas.com/cat/says/Sleepy",
        "https://cataas.com/cat/says/Angry",
        "https://cataas.com/cat/says/Good%20Morning",
        "https://cataas.com/cat/says/Good%20Night",
        "https://cataas.com/cat/says/Meow%20Meow",
        "https://cataas.com/cat/says/Rawr",
        "https://cataas.com/cat/says/Monday",
        "https://cataas.com/cat/says/Friday",
        "https://cataas.com/cat/says/Sunday",
        "https://cataas.com/cat/says/Cat", "https://cataas.com/cat/says/Lazy",
        "https://cataas.com/cat/says/Play", "https://cataas.com/cat/says/Nope",
        "https://cataas.com/cat/says/Yes", "https://cataas.com/cat/says/Ok",
        "https://cataas.com/cat/says/Why", "https://cataas.com/cat/says/What",
        "https://cataas.com/cat/says/When", "https://cataas.com/cat/says/How",
        "https://cataas.com/cat/says/Who", "https://cataas.com/cat/says/Where",
        "https://cataas.com/cat/says/Sure",
        "https://cataas.com/cat/says/Maybe",
        "https://cataas.com/cat/says/Sorry",
        "https://cataas.com/cat/says/Thanks",
        "https://cataas.com/cat/says/Friends",
        "https://cataas.com/cat/says/Chill",
        "https://cataas.com/cat/says/Coffee",
        "https://cataas.com/cat/says/Tea", "https://cataas.com/cat/says/Smile",
        "https://cataas.com/cat/says/Fun", "https://cataas.com/cat/says/Work",
        "https://cataas.com/cat/says/Study",
        "https://cataas.com/cat/says/School",
        "https://cataas.com/cat/says/Weekend",
        "https://cataas.com/cat/says/Holiday",
        "https://cataas.com/cat/says/Cute",
        "https://cataas.com/cat/says/Sweet",
        "https://cataas.com/cat/says/Kawaii",
        "https://cataas.com/cat/says/Nice",
        "https://cataas.com/cat/says/Beautiful",
        "https://cataas.com/cat/says/Cool",
        "https://cataas.com/cat/says/Lovely",
        "https://cataas.com/cat/says/Great",
        "https://cataas.com/cat/says/Best", "https://cataas.com/cat/says/Wow",
        "https://cataas.com/cat/says/Yay", "https://cataas.com/cat/says/Omg",
        "https://cataas.com/cat/says/Uwu", "https://cataas.com/cat/says/Owo",
        "https://cataas.com/cat/says/Yeah", "https://cataas.com/cat/says/Nooo",
        "https://cataas.com/cat/says/Bye",
        "https://cataas.com/cat/says/Hi%20Again",
        "https://cataas.com/cat/says/Welcome",
        "https://cataas.com/cat/says/Peace", "https://cataas.com/cat/says/Bro",
        "https://cataas.com/cat/says/Sis", "https://cataas.com/cat/says/Bae",
        "https://cataas.com/cat/says/Lmao", "https://cataas.com/cat/says/Lol",
        "https://cataas.com/cat/says/Haha", "https://cataas.com/cat/says/Hehe",
        "https://cataas.com/cat/says/Hihi",
        "https://cataas.com/cat/says/Random",
        "https://cataas.com/cat/says/Why%20Not",
        "https://cataas.com/cat/says/IDK", "https://cataas.com/cat/says/WTF",
        "https://cataas.com/cat/says/WOWWW", "https://cataas.com/cat/says/YEP",
        "https://cataas.com/cat/says/NOPEE", "https://cataas.com/cat/says/Ugh",
        "https://cataas.com/cat/says/Meh",
        "https://cataas.com/cat/says/Fat%20Cat",
        "https://cataas.com/cat/says/Skinny%20Cat",
        "https://cataas.com/cat/says/Big%20Cat",
        "https://cataas.com/cat/says/Tiny%20Cat",
        "https://cataas.com/cat/says/Happy%20Cat",
        "https://cataas.com/cat/says/Sad%20Cat",
        "https://cataas.com/cat/says/Angry%20Cat",
        "https://cataas.com/cat/says/Lazy%20Cat",
        "https://cataas.com/cat/says/Sleepy%20Cat",
        "https://cataas.com/cat/says/Crazy%20Cat",
        "https://cataas.com/cat/says/Smart%20Cat",
        "https://cataas.com/cat/says/Dumb%20Cat",
        "https://cataas.com/cat/says/King%20Cat",
        "https://cataas.com/cat/says/Queen%20Cat",
        "https://cataas.com/cat/says/Boss%20Cat",
        "https://cataas.com/cat/says/Legendary%20Cat",
        "https://cataas.com/cat/says/Meme%20Cat",
        "https://cataas.com/cat/says/Real%20Cat"
    ]
    await update.message.reply_photo(random.choice(cats))


# /love
async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        nama1 = context.args[0]
        nama2 = context.args[1]
        persen = random.randint(1, 100)
        await update.message.reply_text(
            f"Kecocokan {nama1} ❤️ {nama2}: {persen}%")
    else:
        await update.message.reply_text("Contoh: /love Andi Budi")


async def tebakangka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    number = random.randint(1, 100)
    GAME_STATE[user_id] = number
    await update.message.reply_text(
        "🎲 Aku sudah milih angka 1-100. Tebak dengan kirim angkanya!")


async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in GAME_STATE:
        try:
            guess = int(update.message.text.strip())
            target = GAME_STATE[user_id]
            if guess < target:
                await update.message.reply_text("🔻 Terlalu kecil!")
            elif guess > target:
                await update.message.reply_text("🔺 Terlalu besar!")
            else:
                await update.message.reply_text("✅ Benar! Kamu menang!")
                del GAME_STATE[user_id]
        except ValueError:
            pass


async def tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        text = " ".join(context.args)
        try:
            # Generate speech
            tts = gTTS(
                text=text, lang='id'
            )  # 'id' buat bahasa Indonesia, ganti 'en' kalau mau Inggris
            filename = f"tts_{update.effective_user.id}.mp3"
            tts.save(filename)

            # Kirim sebagai voice note (opus/ogg)
            with open(filename, 'rb') as audio:
                await update.message.reply_voice(voice=audio,
                                                 caption="🎤 Nih suaranya:")

            os.remove(filename)  # bersihin file setelah dikirim
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error generate TTS: {str(e)}")
    else:
        await update.message.reply_text("Contoh: /tts Halo dunia")


async def stickerify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /stickerify Teksnya apa")
        return

    text = " ".join(context.args)

    # Load font
    font_path = os.path.join("fonts", "Arial-Narrow-Regular.ttf")
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)

    # Hitung ukuran teks
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Bikin gambar dengan background putih
    size = max(text_width, text_height) + 40
    img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))

    # Convert ke webp (Telegram sticker format)
    output = io.BytesIO()
    img.save(output, format='WEBP')
    output.seek(0)

    await update.message.reply_sticker(sticker=output)


# Tambahin ke bot
async def lyrics_genius_api(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Contoh: /lyrics Genius sia:API Cheap Thrills")
        return

    query = " ".join(context.args)

    await update.message.reply_text(f"🔍 Cari lirik: {query}...")

    try:
        headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
        params = {'q': query}
        response = requests.get("https://api.genius.com/search",
                                headers=headers,
                                params=params,
                                timeout=10)
        data = response.json()

        hits = data['response']['hits']
        if not hits:
            await update.message.reply_text("❌ Lagu nggak ketemu.")
            return

        # Ambil lagu pertama
        song = hits[0]['result']
        song_title = song['title']
        artist = song['primary_artist']['name']
        url = song['url']

        # Scrape lirik dari halaman
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        lyrics_divs = soup.select("div[data-lyrics-container=true]")
        lyrics = "\n".join(
            [div.get_text(separator="\n") for div in lyrics_divs])

        if not lyrics.strip():
            lyrics = "(⚠️ Lirik nggak bisa diambil. Mungkin protected.)"

        text = f"🎵 *{song_title}* by *{artist}*\n\n{lyrics[:4000]}"
        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")


async def lyrics_genius_scraping(update: Update,
                                 context: ContextTypes.DEFAULT_TYPE):
    try:
        args_joined = " ".join(context.args)
        # Misalnya: Genius sia:scraping Cheap Thrills
        parts = args_joined.split(':scraping')
        if len(parts) != 2:
            await update.message.reply_text(
                "Format salah. Contoh: /lyrics Genius sia:scraping Cheap Thrills"
            )
            return

        artist_part = parts[0].replace("Genius", "").strip()
        query_part = parts[1].strip()
        search_query = f"{artist_part} {query_part}"

        await update.message.reply_text(f"🔍 Scraping lirik: {search_query}...")

        # Step 1: Cari di Genius pake search URL
        search_url = f"https://genius.com/api/search/multi?per_page=5&q={requests.utils.quote(search_query)}"
        resp = requests.get(search_url, timeout=10)
        data = resp.json()

        hits = data['response']['sections'][0]['hits']
        if not hits:
            await update.message.reply_text("❌ Lagu nggak ketemu di Genius.")
            return

        song_url = hits[0]['result']['url']

        # Step 2: Scrape halaman lirik
        page = requests.get(song_url, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        lyrics_divs = soup.select("div[data-lyrics-container=true]")
        lyrics = "\n".join(
            [div.get_text(separator="\n") for div in lyrics_divs])

        if not lyrics.strip():
            lyrics = "(⚠️ Lirik nggak bisa diambil. Mungkin protected.)"

        title = hits[0]['result']['title']
        artist = hits[0]['result']['primary_artist']['name']

        text = f"🎵 *{title}* by *{artist}*\n\n{lyrics[:4000]}"
        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error scraping: {str(e)}")


async def lyrics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Contoh: /lyrics Genius sia:API Cheap Thrills")
        return

    args_joined = " ".join(context.args)

    if ":API" in args_joined:
        await lyrics_genius_api(update, context)
    elif ":scraping" in args_joined:
        await lyrics_genius_scraping(update, context)
    else:
        await update.message.reply_text(
            "⚠️ Tambahin :API atau :scraping di perintahmu.")


async def define(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /define serendipity")
        return
    word = context.args[0]
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        try:
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
            part_of_speech = data[0]['meanings'][0]['partOfSpeech']
            await update.message.reply_text(
                f"{word} ({part_of_speech}): {meaning}")
        except (KeyError, IndexError):
            await update.message.reply_text("Definisi nggak ketemu.")
    else:
        await update.message.reply_text("Definisi nggak ketemu.")


async def biner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Contoh: /biner Hamzah atau /biner 01001000...")
        return

    inp = " ".join(context.args).strip()

    # Cek apakah input full 0 dan 1
    if all(c in "01" for c in inp.replace(" ", "")) and len(
            inp.replace(" ", "")) % 8 == 0:
        # Biner ke teks
        try:
            chars = [chr(int(inp[i:i + 8], 2)) for i in range(0, len(inp), 8)]
            hasil = ''.join(chars)
            await update.message.reply_text(hasil)
        except:
            await update.message.reply_text("❌ Format biner salah.")
    else:
        # Teks ke biner
        hasil = ''.join(format(ord(c), '08b') for c in inp)
        await update.message.reply_text(hasil)


async def belajar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /belajar 10 detik lagi")
        return

    teks = " ".join(context.args).lower()
    match = re.match(r"(\d+)\s*(detik|menit|jam)", teks)

    if not match:
        await update.message.reply_text(
            "Format salah. Contoh: /belajar 5 detik lagi")
        return

    jumlah = int(match.group(1))
    satuan = match.group(2)

    if satuan == "detik":
        delay = jumlah
    elif satuan == "menit":
        delay = jumlah * 60
    elif satuan == "jam":
        delay = jumlah * 3600
    else:
        await update.message.reply_text("Satuan waktu gak dikenali.")
        return

    await update.message.reply_text(
        f"⏰ Oke, akan ngingetin kamu belajar dalam {jumlah} {satuan}...")

    # Jalanin delay tanpa ngeblok bot
    async def kirim_notif():
        await asyncio.sleep(delay)
        await update.message.reply_text("📚 BELAJAR WOYYY!!!")

    asyncio.create_task(kirim_notif())


import json


def simpan_keuangan(jenis, jumlah, keterangan, user_id):
    try:
        with open("keuangan.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    uid = str(user_id)
    if uid not in data:
        data[uid] = []

    data[uid].append({
        "jenis": jenis,
        "jumlah": jumlah,
        "keterangan": keterangan
    })

    with open("keuangan.json", "w") as f:
        json.dump(data, f, indent=2)


async def welcome_on_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status == "member":
        keyboard = [["💰 Keuangan"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Halo, siap bantu keuangan lo.",
                                       reply_markup=reply_markup)


async def keuangan_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["➕ Pemasukan", "➖ Pengeluaran"], ["❌ Batal"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Pilih transaksi:",
                                    reply_markup=reply_markup)
    context.user_data["mode"] = "menu_keuangan"


async def transaksi_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    if mode == "menu_keuangan":
        text = update.message.text
        if text == "➕ Pemasukan":
            context.user_data["mode"] = "pemasukan"
            await update.message.reply_text(
                "Masukkan jumlah & keterangan: 50000 Gaji part time")
        elif text == "➖ Pengeluaran":
            context.user_data["mode"] = "pengeluaran"
            await update.message.reply_text(
                "Masukkan jumlah & keterangan: 20000 Beli jajan")
        elif text == "❌ Batal":
            context.user_data.clear()
            await update.message.reply_text("❌ Dibatalkan")
    elif mode in ["pemasukan", "pengeluaran"]:
        try:
            jumlah_str, *ket = update.message.text.strip().split()
            jumlah = int(jumlah_str)
            keterangan = " ".join(ket)
            jenis = "masuk" if mode == "pemasukan" else "keluar"
            simpan_keuangan(jenis, jumlah, keterangan,
                            update.effective_user.id)
            await update.message.reply_text(
                f"✅ {jenis.upper()} Rp{jumlah:,} dicatat!\n📌 {keterangan}")
            context.user_data.clear()
        except:
            await update.message.reply_text(
                "❌ Format salah. Contoh: 30000 Bayar listrik")


async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    username = user.username or user.full_name

    print(f"[DEBUG] Telegram ID kamu: {uid}"
          )  # <--- ini penting, muncul di terminal

    data = load_user_data()

    # Auto-register kalau user belum ada
    if uid not in data:
        data[uid] = {"username": username, "poin": 20}
        save_user_data(data)

    user_data = data[uid]

    await update.message.reply_text(f"👤 Username: {user_data['username']}\n"
                                    f"💎 Poin: {user_data['poin']}")


def load_user_data():
    if not os.path.exists("data_user.json"):
        return {}
    with open("data_user.json", "r") as f:
        return json.load(f)


def save_user_data(data):
    with open("data_user.json", "w") as f:
        json.dump(data, f, indent=2)


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os, shutil, zipfile, uuid


async def scrape_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_or_create_user(user.id, user.username or user.full_name)

    if user_data["poin"] < 10:
        await update.message.reply_text(
            "❌ Poin kamu kurang buat scrape (butuh 10 poin).")
        return

    if not context.args:
        await update.message.reply_text("Contoh: /scrape https://example.com")
        return

    url = context.args[0]
    await update.message.reply_text(f"🔍 Sedang scrape: {url}")

    # Buat folder scrape unik
    folder_id = str(uuid.uuid4())[:8]
    base_folder = f"scrape_{folder_id}"
    os.makedirs(base_folder, exist_ok=True)

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Simpan HTML
        with open(os.path.join(base_folder, "index.html"),
                  "w",
                  encoding="utf-8") as f:
            f.write(soup.prettify())

        # Download asset eksternal (css/js/img)
        for tag in soup.find_all(["link", "script", "img"]):
            attr = "href" if tag.name == "link" else "src"
            src = tag.get(attr)
            if not src:
                continue

            asset_url = urljoin(url, src)
            filename = os.path.basename(urlparse(asset_url).path)
            if not filename:
                continue
            try:
                file_path = os.path.join(base_folder, filename)
                with open(file_path, "wb") as f:
                    f.write(requests.get(asset_url, timeout=5).content)
            except:
                continue

        # Buat ZIP
        zipname = f"{base_folder}.zip"
        with zipfile.ZipFile(zipname, "w") as zipf:
            for root, dirs, files in os.walk(base_folder):
                for file in files:
                    path = os.path.join(root, file)
                    zipf.write(path,
                               arcname=os.path.relpath(path, base_folder))

        # Kirim ke user
        with open(zipname, "rb") as f:
            await update.message.reply_document(f, filename=zipname)

        # Potong 10 poin
        user_data["poin"] -= 10
        data = load_user_data()
        data[str(user.id)] = user_data
        save_user_data(data)

        await update.message.reply_text(
            f"✅ Scrape selesai! 💎 Poin tersisa: {user_data['poin']}")

    except Exception as e:
        await update.message.reply_text(f"❌ Gagal scrape: {e}")

    finally:
        shutil.rmtree(base_folder, ignore_errors=True)
        if os.path.exists(zipname):
            os.remove(zipname)


def get_or_create_user(user_id, username):
    uid = str(user_id)
    data = load_user_data()

    if uid not in data:
        data[uid] = {"username": username, "poin": 20}
        save_user_data(data)

    return data[uid]


async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "❌ Contoh: /ai siapa presiden pertama indonesia")
        return

    user_input = " ".join(context.args)
    try:
        url = f"https://api.siputzx.my.id/api/ai/deepseek-llm-67b-chat?content={user_input}"
        res = requests.get(url)
        data = res.json()

        if data["status"]:
            await update.message.reply_text(f"{data['data']}")
        else:
            await update.message.reply_text("❌ Gagal dapetin respon dari AI.")
    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))


async def gemini_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Contoh: /gemini apa itu bot?")
        return

    question = " ".join(context.args).strip()

    url = f'https://api.siputzx.my.id/api/ai/gemini-pro?content={question}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # cek format data, contoh: {"message":"jawaban"}
                    answer = data.get("message", "❓ Jawaban tidak ditemukan.")
                    await update.message.reply_text(
                        f'🤖 **Gemini says:**\n{answer}', parse_mode="Markdown")
                else:
                    await update.message.reply_text(
                        f"❌ API error: status {resp.status}")
    except Exception as e:
        await update.message.reply_text(f"🚫 Gagal menghubungi API: {e}")


OWNER_ID = "8046782026"  # pasang di atas, bareng import

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = "8046782026"  # ganti sesuai ID kamu


async def igstalk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Contoh: /igstalk username")
        return

    target_username = context.args[0].strip()

    url = f"https://api.siputzx.my.id/api/stalk/instagram?username={target_username}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data_api = await resp.json()
                    d = data_api.get("data", {})

                    if not d:
                        await update.message.reply_text(
                            "❌ Data kosong atau user tidak ditemukan.")
                        return

                    # Data profil utama
                    profil_text = f"""
👤 *Username*: `{d.get('username', '-')}`
📛 *Full Name*: {d.get('full_name', '-')}
📝 *Bio*: {d.get('biography', '-')}
🌐 *Website*: {d.get('external_url', '-') or '-'}
📷 *Posts*: {d.get('posts_count', '-')}
👥 *Followers*: {d.get('followers_count', '-')}
👣 *Following*: {d.get('following_count', '-')}
🔒 *Private*: {d.get('is_private', '-')}
✅ *Verified*: {d.get('is_verified', '-')}
"""

                    await update.message.reply_photo(photo=d.get(
                        'profile_pic_url', ''),
                                                     caption=profil_text,
                                                     parse_mode="Markdown")

                    # === Bagian postingan ===
                    posts = d.get("posts", [])
                    if posts:
                        await update.message.reply_text(
                            f"📸 *{len(posts)} Postingan Terbaru:*",
                            parse_mode="Markdown")
                        for idx, post in enumerate(
                                posts[:5],
                                1):  # Biar ga kebanyakan, ambil 5 post
                            caption = post.get("caption", "-")
                            shortcode = post.get("shortcode", "")
                            post_url = f"https://www.instagram.com/p/{shortcode}" if shortcode else "-"
                            media = post.get("media_url") or post.get(
                                "thumbnail_url") or ""

                            text_post = f"""
📦 *Post #{idx}*
💬 *Caption*: {caption}
🔗 [Buka Postingan IG]({post_url})
"""
                            if media:
                                await update.message.reply_photo(
                                    photo=media,
                                    caption=text_post,
                                    parse_mode="Markdown")
                            else:
                                await update.message.reply_text(
                                    text_post, parse_mode="Markdown")
                    else:
                        await update.message.reply_text(
                            "❔ Tidak ada postingan terbaru yang bisa ditampilkan."
                        )
                else:
                    await update.message.reply_text(
                        f"❌ API error: status {resp.status}")
    except Exception as e:
        await update.message.reply_text(f"🚫 Gagal hubungi API: {e}")


OWNER_ID = "8046782026"  # ganti sesuai punyamu

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = "8046782026"  # ganti sesuai ID kamu

import aiohttp
import json
import os
from telegram import Update
from telegram.ext import ContextTypes

# Ganti sama ID kamu
OWNER_ID = "8046782026"


# === YTMP3 command ===
async def ytmp3_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if not context.args:
        await update.message.reply_text(
            "⚠️ Contoh: /ytmp3 https://youtu.be/abc123")
        return

    yt_url = context.args[0].strip()

    data = load_user_data()
    if uid not in data:
        await update.message.reply_text(
            "❌ Kamu belum terdaftar. Gunakan /user dulu.")
        return

    points = data[uid].get("poin", 0)

    if uid == OWNER_ID:
        pass  # owner gratis
    else:
        if points < 1:
            await update.message.reply_text(
                f"⚡️ Point kamu kurang ({points}). Perlu 1 point untuk pakai perintah ini."
            )
            return
        data[uid]["poin"] -= 1
        save_user_data(data)

    api_url = f"https://api.siputzx.my.id/api/dl/youtube/mp3?url={yt_url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data_api = await resp.json()
                    result = data_api.get("data") or {}

                    title = result.get("title", "Unknown")
                    dl_url = result.get("url") or result.get("link") or ""

                    if not dl_url:
                        await update.message.reply_text(
                            "❌ Gagal ambil link download.")
                        return

                    text = f"🎵 *{title}*\n[Klik untuk download MP3]({dl_url})"
                    await update.message.reply_text(text,
                                                    parse_mode="Markdown")
                else:
                    await update.message.reply_text(
                        f"❌ API error: status {resp.status}")
    except Exception as e:
        await update.message.reply_text(f"🚫 Gagal menghubungi API: {e}")


async def gacha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    data = load_user_data()

    if uid not in data:
        await update.message.reply_text(
            "❌ Kamu belum terdaftar. Gunakan /user dulu.")
        return

    # Gacha antara -500 s/d +1000
    hasil_gacha = random.randint(-500, 1000)

    # Tambah ke poin user
    data[uid]["poin"] = data[uid].get("poin", 0) + hasil_gacha
    save_user_data(data)

    await update.message.reply_text(
        f"🎰 Kamu menggacha: {hasil_gacha} point!\n"
        f"💰 Total point kamu sekarang: {data[uid]['poin']}")


async def stickerify_handler(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.photo:
        await message.reply_text("⚠️ Kirim foto dengan caption .s")
        return

    # Ambil file id foto resolusi tertinggi
    file_id = message.photo[-1].file_id
    file = await context.bot.get_file(file_id)
    file_path = "temp_photo.jpg"
    webp_path = "temp_sticker.webp"

    try:
        # Download file
        await file.download_to_drive(file_path)

        # Convert ke webp (512x512)
        img = Image.open(file_path).convert("RGBA")
        img.thumbnail((512, 512))
        img.save(webp_path, "WEBP")

        # Kirim stiker
        with open(webp_path, "rb") as sticker_file:
            await context.bot.send_sticker(chat_id=message.chat_id,
                                           sticker=sticker_file)

        # Cleanup
        os.remove(file_path)
        os.remove(webp_path)

    except Exception as e:
        await message.reply_text(f"❌ Gagal bikin stiker: {e}")


async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👨‍💻 *Developer Bot*  
• 🪪 *Nama*: Hamzah Wisnu Dzaky  
• 🏫 *Status*: Pelajar kelas 8 SMP  
• ✏ *Hobi*: Ngoding, nyelesaiin math problems, belajar hal baru.  
• 📍 *Lokasi*: Indonesia 🇮🇩  
• 💡 *Motto hidup*: "The more you learn, the more you earn"
"""
    await update.message.reply_text(text, parse_mode="Markdown")


async def replay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Contoh: /replay trigger response")
        return

    trigger = context.args[0].lower()
    response = " ".join(context.args[1:])

    # Cek developer
    if user_id != str(OWNER_ID):
        user_info = data.get(user_id)
        if not user_info or user_info.get("poin", 0) < 5:
            await update.message.reply_text(
                f"❌ Poin kamu nggak cukup! Kamu punya {user_info.get('poin', 0) if user_info else 0} poin (butuh 5)"
            )
            return
        # Kurangi poin
        user_info["poin"] -= 5
        data[user_id] = user_info
        save_data(data)

    # Simpan auto-reply
    replies = load_replies()
    replies[trigger] = response
    save_replies(replies)

    await update.message.reply_text(
        f"✅ Auto-reply *{trigger}* disimpan.\n💰 Sisa poin: {data.get(user_id, {}).get('poin', 0)}",
        parse_mode="Markdown")


async def auto_reply_handler(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    replies = load_replies()
    if text in replies:
        await update.message.reply_text(replies[text])


# ===== text_handler.py atau taruh di main.py sekalian =====
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    # Cek tebak angka dulu
    if user_id in GAME_STATE:
        await handle_guess(update, context)
        return

    # Auto reply
    replies = load_replies()
    if text in replies:
        await update.message.reply_text(replies[text])
        return

    # Cek menu keuangan
    if text == "💰 keuangan":
        await keuangan_menu(update, context)
        return

    # Default fallback: transaksi input
    await transaksi_input(update, context)


import logging

logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.error(msg="Exception while handling update:",
                 exc_info=context.error)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.siputzx.my.id/api/berita/cnbcindonesia"

    try:
        resp = requests.get(url)
        data = resp.json()

        if "result" in data and data["result"]:
            reply = "📰 *Berita CNBC Hari Ini:*\n\n"
            for item in data["result"][:5]:  # ambil 5 berita teratas
                reply += f"• [{item['title']}]({item['link']})\n"

            await update.message.reply_text(reply,
                                            parse_mode="Markdown",
                                            disable_web_page_preview=True)
        else:
            await update.message.reply_text("Gagal ambil berita atau kosong.")

    except Exception as e:
        await update.message.reply_text("⚠️ Error ambil berita.")
        print(f"NEWS ERROR: {e}")


async def qc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = str(update.effective_user.id)
    text = ' '.join(context.args)

    if not text:
        await message.reply_text("⚠️ Contoh: /qc halo dunia")
        return

    # Load data poin user
    data = load_data()
    user_info = data.get(user_id)

    if not user_info or user_info.get("poin", 0) < 4:
        await message.reply_text(
            f"❌ Poin kamu nggak cukup! Kamu punya {user_info.get('poin', 0) if user_info else 0} poin (butuh 4)"
        )
        return

    # Kurangi 4 poin
    user_info["poin"] -= 4
    data[user_id] = user_info
    save_data(data)

    # Ambil username
    username = update.effective_user.username or update.effective_user.first_name

    # Ambil foto profil user
    photos = await context.bot.get_user_profile_photos(
        update.effective_user.id, limit=1)
    if photos.total_count > 0:
        photo_file = await photos.photos[0][0].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        avatar = Image.open(BytesIO(photo_bytes)).convert("RGBA")
    else:
        avatar = Image.new("RGBA", (100, 100),
                           (200, 200, 200, 255))  # default gray

    avatar = avatar.resize((100, 100))

    # Buat background putih
    img = Image.new("RGBA", (600, 200), "WHITE")
    draw = ImageDraw.Draw(img)

    # Font
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 24)

    # Tempel avatar kiri
    img.paste(avatar, (20, 50))

    # Tulis username
    draw.text((140, 50), f"@{username}", font=font_big, fill="black")

    # Tulis pesan
    draw.text((140, 100), text, font=font_small, fill="black")

    # Save ke webp
    output = BytesIO()
    img.save(output, format="WEBP")
    output.seek(0)

    await message.reply_sticker(sticker=output)
    await message.reply_text(
        f"✅ Stiker dibuat! 💰 Sisa poin: {user_info['poin']}")


async def whois_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    user_info = data.get(user_id)

    if not user_info or user_info.get("poin", 0) < 15:
        await update.message.reply_text(
            f"❌ Poin kamu nggak cukup! Kamu punya {user_info.get('poin', 0) if user_info else 0} poin (butuh 15)"
        )
        return

    if not context.args:
        await update.message.reply_text("⚠️ Contoh: /whois google.com")
        return

    domain = context.args[0].lower()

    try:
        # Panggil ipapi.is API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipapi.is/{domain}?json")
        info = response.json()

        # Download logo pakai Clearbit
        logo_url = f"https://logo.clearbit.com/{domain}"
        async with httpx.AsyncClient() as client:
            logo_response = await client.get(logo_url)
        logo_bytes = BytesIO(logo_response.content)

        # Biar ga error kalau field kosong
        def get(field):
            return info.get(field) or "-"

        caption = f"""🌐 **Whois Info**
📦 Domain: `{get('domain')}`
🔒 Protocol: {"HTTPS" if "https" in domain else "HTTP"}`
📍 IP: `{get('ip')}`
🏢 Server: `{get('server')}`
📝 Registrar: `{get('registrar')}`
📅 Created: `{get('created')}`
📅 Updated: `{get('updated')}`
📅 Expiry: `{get('expiry')}`

🌎 Country: `{get('country')}`
🏙 Region: `{get('region')}`
🏙 City: `{get('city')}`
🛰 Lat/Lon: `{get('latitude')}, {get('longitude')}`
🕒 Timezone: `{get('timezone')}`
🌐 Continent: `{get('continent')}`

💰 Sisa poin: `{user_info.get('poin', 0)-15}`
"""

        # Kirim foto logo + caption
        await update.message.reply_photo(photo=logo_bytes,
                                         caption=caption,
                                         parse_mode="Markdown")

        # Kurangi poin
        user_info["poin"] -= 15
        data[user_id] = user_info
        save_data(data)

    except Exception as e:
        logger.error(f"[whois_command] Error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def portscan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    user_info = data.get(user_id)

    if not user_info or user_info.get("poin", 0) < 20:
        await update.message.reply_text(
            f"❌ Poin kamu nggak cukup! Kamu punya {user_info.get('poin', 0) if user_info else 0} poin (butuh 20)"
        )
        return

    if not context.args:
        await update.message.reply_text("⚠️ Contoh: /portscan 8.8.8.8")
        return

    target = context.args[0]

    # Port populer untuk fast scan (20-30 port aja, biar cepet)
    fast_ports = [
        21, 22, 23, 25, 53, 80, 110, 123, 143, 161, 194, 443, 465, 587, 993,
        995, 3306, 3389, 5900, 8080
    ]
    open_ports = []

    await update.message.reply_text(f"🛰 Mulai scanning {target}... (Fast mode)"
                                    )

    try:
        for port in fast_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                continue

        ports_text = ", ".join(
            str(p)
            for p in open_ports) if open_ports else "Tidak ada port terbuka"

        await update.message.reply_text(f"""✅ **Scan Selesai**
🌐 Target: `{target}`
🚀 Mode: Fast Scan
📦 Open ports: `{ports_text}`
💰 Sisa poin: `{user_info.get('poin', 0)-20}`
""",
                                        parse_mode="Markdown")

        # Kurangi poin & save
        user_info["poin"] -= 20
        data[user_id] = user_info
        save_data(data)

    except Exception as e:
        logger.error(f"[portscan_command] Error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def jadwal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Contoh: /jadwal senin")
        return

    hari = context.args[0].lower()
    teks = jadwal_kelas_8a.get(hari)

    if teks:
        await update.message.reply_text(teks, parse_mode='Markdown')
        logger.info(f"✅ User minta jadwal {hari}")
    else:
        await update.message.reply_text(teks, parse_mode='MarkdownV2')
        logger.warning(f"❌ User minta jadwal tak dikenal: {hari}")


def main():
    app = Application.builder().token(TOKEN).build()

    # === COMMAND HANDLERS ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("helpall", helpall_command))
    app.add_handler(CommandHandler("help", helpall_command))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("roast", roast))
    app.add_handler(CommandHandler("truth", truth))
    app.add_handler(CommandHandler("dare", dare))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("8ball", eight_ball))
    app.add_handler(CommandHandler("cat", cat))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("tebakangka", tebakangka))
    app.add_handler(CommandHandler("tts", tts))
    app.add_handler(CommandHandler("stickerify", stickerify))
    app.add_handler(CommandHandler("biner", biner))
    app.add_handler(CommandHandler("define", define))
    app.add_handler(CommandHandler("belajar", belajar))
    app.add_handler(CommandHandler("lyrics", lyrics_command))
    app.add_handler(CommandHandler("user", user_info))
    app.add_handler(CommandHandler("scrape", scrape_command))
    app.add_handler(CommandHandler("ai", ai_handler))
    app.add_handler(CommandHandler("gemini", gemini_command))
    app.add_handler(CommandHandler("igstalk", igstalk_command))
    app.add_handler(CommandHandler("ytmp3", ytmp3_command))
    app.add_handler(CommandHandler("gacha", gacha_command))
    app.add_handler(CommandHandler("dev", dev_command))
    app.add_handler(CommandHandler("replay", replay_command))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("qc", qc_command))
    app.add_handler(CommandHandler("whois", whois_command))
    app.add_handler(CommandHandler("portscan", portscan_command))
    app.add_handler(CommandHandler("jadwal", jadwal_handler))

    # Sticker photo trigger
    app.add_handler(
        MessageHandler(filters.PHOTO & filters.CaptionRegex(r"^\.s$"),
                       stickerify_handler))

    # Welcome handler
    app.add_handler(
        ChatMemberHandler(welcome_on_open, ChatMemberHandler.MY_CHAT_MEMBER))

    # === TEXT HANDLER (gabungan) ===
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
