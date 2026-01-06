# 🤖 VClass Unila Telegram Bot

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-async-green)
![Telegram Bot](https://img.shields.io/badge/telegram-bot-blue)
![Status](https://img.shields.io/badge/status-production--ready-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Bot Telegram pribadi untuk **mengecek tugas yang belum dikumpulkan** di  
**VClass Unila (Moodle-based)** secara otomatis.

---

## ✨ Fitur Utama

- 🔐 Login otomatis ke VClass Unila
- 📚 Validasi course (hanya course yang enrolled)
- 📝 Deteksi tugas **belum dikumpulkan**
- 🚦 Skip course enrol page & halaman tidak valid
- ⏳ Progress realtime di Telegram (menampilkan course yang sedang dicek)
- 📊 Ringkasan total + detail per course
- 🔗 Link langsung ke setiap tugas
- 🧪 Debug log tetap aktif di console
- 🤖 Bot **private** (hanya 1 Telegram User ID)

---

## 📌 Contoh Output Telegram

```
📌 RINGKASAN TUGAS BELUM DIKUMPULKAN

Total: 5 tugas

📘 PSTI Logika
- 2 tugas
  • Tugas 1
    🔗 https://...
  • Tugas 3
    🔗 https://...

📗 Basis Data
- 3 tugas
  • ERD
    🔗 https://...
  • Normalisasi
    🔗 https://...
  • Query
    🔗 https://...
```

---

## 🧠 Alur Kerja Bot

```
/start
  → Validasi login VClass
  → Session OK

/cek
  → Scan semua course
  → Cek assignment
  → Kirim hasil ke Telegram
```

---

## 🗂️ Struktur Project

```
vclass-telegram-bot/
│
├─ bot.py
├─ moodle.py
├─ req.txt
├─ .env
└─ README.md
```

---

## ⚙️ Instalasi

```bash
pip install -r req.txt
playwright install chromium
```

---

## 🔐 Konfigurasi `.env`

```env
BOT_TOKEN=TOKEN_BOT_TELEGRAM
TELEGRAM_USER_ID=123456789

VCLASS_USERNAME=USERNAME_VCLASS
VCLASS_PASSWORD=PASSWORD_VCLASS
```

---

## ▶️ Menjalankan Bot

```bash
python bot.py
```

---

## 🤖 Perintah Telegram

| Command | Fungsi |
|------|------|
| `/start` | Validasi akun VClass |
| `/cek` | Cek tugas |

---

## 🔒 Keamanan

- Bot hanya merespon **1 Telegram User ID**
- Credential disimpan via `.env`
- Tidak menyimpan data ke database

---

## 📜 Lisensi

MIT License

---

## 🙌 Author
ChatGPT 
KepoX
