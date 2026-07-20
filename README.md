# MediaAuto 🤖

پروژه خودکار سازی انتشار محتوا از منابع مختلف به تلگرام با قابلیت ویرایش و مدیریت هوشمند.

## ✨ امکانات

- 🔄 **دریافت خودکار محتوا** از تلگرام، اینستاگرام، یوتیوب، تیک‌تاک، فیسبوک و X
- ✏️ **ویرایش خودکار کپشن** - حذف آیدی‌ها، لینک‌ها، تبلیغات و هشتگ‌های اضافی
- 🚫 **جلوگیری از تکرار** - ذخیره خودکار هش محتوا برای جلوگیری از پست‌های تکراری
- ⏰ **زمان‌بندی انتشار** - 5، 10، 30 دقیقه یا هر ساعت یا دستی
- 🤖 **بازنویسی با AI** - کوتاه‌تر، جذاب‌تر و با ایموجی
- 🎬 **دانلود خودکار رسانه‌ها** - عکس، ویدیو�� گیف و فایل‌های بزرگ
- 🌐 **پنل مدیریت تحت وب** - مدیریت منابع، تنظیمات و بررسی وضعیت
- 🔐 **پشتیبانی برای کانال‌های خصوصی** - با احتمال Telethon
- 📊 **داشبورد و آمار** - تعداد پست‌های ارسالی، خطاها و گزارش‌های تفصیلی
- 📝 **لاگ کامل** - ثبت تمام عملیات برای رفع مشکلات

## 🚀 شروع سریع

### پیش‌نیازها

- Ubuntu 22 یا 24
- Python 3.10+
- اتصال اینترنت

### نصب با یک دستور

```bash
git clone https://github.com/0919shah0-cloud/MediaAuto.git
cd MediaAuto
chmod +x install.sh
./install.sh
```

اسکریپت نصب تمام موارد زیر را درخواست می‌کند:

1. **توکن ربات تلگرام** - از [@BotFather](https://t.me/BotFather)
2. **API ID و API HASH** - از [my.telegram.org](https://my.telegram.org)
3. **شماره تلفن تلگرام** - برای ورود Telethon
4. **کد تایید و رمز دوتایی** - اگر فعال است
5. **کانال‌های منبع** - لیست کانال‌هایی برای مانیتور کردن
6. **کانال مقصد** - جایی برای ارسال پست‌ها
7. **تنظیمات دیگر** - متن تبلیغاتی، واترمارک، API کلید‌ها

## 📁 ساختار پروژه

```
MediaAuto/
├── mediaauto/
│   ├── __init__.py
│   ├── main.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── telegram_client.py      # ارتباط Telethon
│   │   ├── message_handler.py      # مدیریت پیام‌ها
│   │   └── posting_scheduler.py    # زمان‌بندی انتشار
│   ├── panel/
│   │   ├── __init__.py
│   │   ├── app.py                  # برنامه Flask/FastAPI
│   │   ├── auth.py                 # احتمال‌ رمز عبور
│   │   ├── routes.py               # مسیرهای API
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── index.html
│   │   └── templates/
│   │       ├── dashboard.html
│   │       ├── sources.html
│   │       ├── scheduler.html
│   │       ├── logs.html
│   │       └── settings.html
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── rewriter.py             # بازنویسی متن
│   │   ├── caption_cleaner.py      # پاکیزه‌سازی کپشن
│   │   └── translator.py           # ترجمه فارسی
│   ├── downloader/
│   │   ├── __init__.py
│   │   ├── instagram_downloader.py
│   │   ├── youtube_downloader.py
│   │   ├── tiktok_downloader.py
│   │   ├── facebook_downloader.py
│   │   ├── twitter_downloader.py
│   │   └── media_processor.py
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── job_scheduler.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                   # اتصال دیتابیس
│   │   └── models.py               # مدل‌های دیتابیس
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py             # تنظیمات اصلی
│   │   ├── config.json             # فایل تنظیمات
│   │   └── secrets.env             # متغیرهای محرمانه
│   └── utils/
│       ├── __init__.py
│       ├── logger.py               # سیستم لاگ
│       ├── validators.py           # تایید ورودی‌ها
│       └── helpers.py              # توابع کمکی
├── tests/
│   ├── __init__.py
│   ├── test_bot.py
│   ├── test_downloader.py
│   └── test_ai.py
├── logs/
│   └── mediaauto.log              # فایل لاگ
├── install.sh                      # اسکریپت نصب تعاملی
├── requirements.txt                # وابستگی‌های Python
├── docker-compose.yml              # تنظیمات Docker
├── systemd.service                 # خدمت سیستمی خودکار
├── config.example.json             # نمونه تنظیمات
└── README.md
```

## 🔧 تنظیمات دستی (اختیاری)

اگر می‌خواهید بعد از نصب تنظیمات را تغییر دهید:

```bash
# ویرایش تنظیمات
nano ~/MediaAuto/config.json

# بازراه‌اندازی سرویس
sudo systemctl restart mediaauto

# بررسی وضعیت
sudo systemctl status mediaauto

# مشاهده لاگ‌ها
tail -f ~/MediaAuto/logs/mediaauto.log
```

## 🌐 دسترسی به پنل مدیریت

بعد از نصب، پنل در این آدرس در دسترس است:

- **آدرس**: `http://YOUR_SERVER_IP:8000`
- **نام کاربری**: `admin`
- **رمز عبور**: تعیین شده در حین نصب

## 📡 API مدیریت

تمام عملیات می‌توانند از طریق API RESTful انجام شوند:

```bash
# دریافت وضعیت
curl http://localhost:8000/api/status

# لیست کانال‌ها
curl http://localhost:8000/api/sources

# افزودن کانال جدید
curl -X POST http://localhost:8000/api/sources \
  -H "Content-Type: application/json" \
  -d '{"url": "@channel_name"}'
```

## 📋 فایل تنظیمات

تنظیمات در فایل `config.json` ذخیره می‌شوند:

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "api_id": "YOUR_API_ID",
  "api_hash": "YOUR_API_HASH",
  "phone_number": "+9899999999",
  "sources": ["@channel1", "@channel2"],
  "destination": "@my_channel",
  "schedule_interval": 30,
  "watermark_text": "@MyChannel",
  "ai_enabled": true,
  "translate_to_persian": true,
  "web_panel_port": 8000,
  "web_panel_username": "admin",
  "web_panel_password": "secure_password"
}
```

## 🐳 نصب با Docker

```bash
docker-compose up -d
```

## 🛠️ عیب‌یابی

### ربات پاسخ نمی‌دهد

1. بررسی توکن ربات:
   ```bash
   grep bot_token config.json
   ```

2. بررسی وضعیت سرویس:
   ```bash
   sudo systemctl status mediaauto
   ```

3. مشاهده لاگ‌ها:
   ```bash
   tail -100 logs/mediaauto.log
   ```

### خطای احتمال (2FA)

اگر تلگرام کد تایید درخواست کرد:

1. لاگ‌ها را بررسی کنید
2. کد را در فایل ورودی وارد کنید
3. اگر رمز دو مرحله‌ای دارید، آن را هم وارد کنید

### مشکل دانلود ویدیو

مطمئن شوید `yt-dlp` نصب است:

```bash
pip install yt-dlp --upgrade
```

## 🔐 امنیت

- تمام توکن‌ها در `secrets.env` ذخیره می‌شوند
- پنل مدیریت با رمز عبور قوی محافظت می‌شود
- هیچ اطلاعات حساس در فایل لاگ ثبت نمی‌شود
- تمام ارتباطات از طریق HTTPS (در production)

## 📝 لایسنس

MIT License

## 👨‍💻 توسعه‌دهنده

0919shah0-cloud

## 💬 پشتیبانی

برای گزارش خطاها و پیشنهادات:

- Issues: [GitHub Issues](https://github.com/0919shah0-cloud/MediaAuto/issues)
- Pull Requests: [GitHub PRs](https://github.com/0919shah0-cloud/MediaAuto/pulls)

---

**نکته**: اگر مشکلی داشتید، ابتدا فایل `README.md` و لاگ‌ها را بررسی کنید، سپس یک Issue جدید باز کنید.
