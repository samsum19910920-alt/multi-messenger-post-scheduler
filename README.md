# Multi-Messenger Post Scheduler

یک سامانه جامع برای زمان‌بندی و ارسال خودکار پست‌ها به پیام‌رسان‌های ایرانی (روبیکا، بله، ایتا، سروش)

## ویژگی‌ها

✅ **احراز هویت امن** - سیستم OTP از طریق SMS
✅ **چند پیام‌رسان** - پشتیبانی از روبیکا، بله، ایتا، سروش
✅ **زمان‌بندی خودکار** - برنامه‌ریزی برای ارسال بعدی
✅ **مدیریت رسانه** - پشتیبانی از تصویر و ویدئو
✅ **حذف خودکار** - حذف فایل‌ها بعد از 7 روز
✅ **پنل مدیریت** - رابط وب برای مدیریت سیستم
✅ **امنیت** - رمزگذاری رمزعبور، JWT، CORS

## ساختار پروژه

```
multi-messenger-post-scheduler/
├── backend/
│   ├── models/              # مدل‌های پایگاه داده
│   ├── routes/              # API endpoints
│   ├── utils/               # توابع کمکی و validators
│   ├── tasks/               # کار‌های زمان‌بندی شده
│   ├── app.py              # تنظیمات Flask
│   └── requirements.txt     # وابستگی‌ها
├── admin-panel/
│   ├── templates/           # صفحات HTML
│   └── static/              # CSS/JS
├── android-app/             # برنامه Android (Kotlin)
├── docs/
│   └── API.md              # مستندات API
├── .env.example            # نمونه متغیرهای محیطی
└── README.md               # این فایل
```

## نصب و راه‌اندازی

### الزامات
- Python 3.8+
- Git
- Android Studio (برای نسخه Android)

### مراحل راه‌اندازی

1. **��لون مخزن**
```bash
git clone https://github.com/yourusername/multi-messenger-post-scheduler.git
cd multi-messenger-post-scheduler
```

2. **ایجاد محیط مجازی**
```bash
python -m venv venv
source venv/bin/activate  # در Windows: venv\Scripts\activate
```

3. **نصب وابستگی‌ها**
```bash
cd backend
pip install -r requirements.txt
```

4. **تنظیم متغیرهای محیطی**
```bash
cp .env.example .env
# سپس .env را ویرایش کنید و مقادیر را وارد کنید
```

5. **راه‌اندازی Backend**
```bash
python app.py
```

Backend در آدرس `http://localhost:5000` اجرا می‌شود.

## مستندات API

برای مستندات کامل API، به [API.md](docs/API.md) مراجعه کنید.

## امنیت

### نکات امنیتی پیاده‌شده:
- ✅ **Hashing رمزعبور** - استفاده از bcrypt
- ✅ **JWT Authentication** - توکن‌های محدود مدت
- ✅ **Input Validation** - بررسی تمام ورودی‌ها
- ✅ **SQL Injection Prevention** - استفاده از ORM
- ✅ **CORS Security** - محدودیت دامنه‌ها
- ✅ **Environment Variables** - مخفی‌سازی کلیدها
- ✅ **Rate Limiting** - در حال توسعه
- ✅ **Secure Storage** - ذخیره‌سازی محفوظ توکن‌ها

## توسعه

### مراحل اولیه توسعه:

1. **ایجاد شاخه برای ویژگی جدید**
```bash
git checkout -b feature/new-feature
```

2. **ارسال تغییرات**
```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

3. **ایجاد Pull Request**

## لایسنس

این پروژه تحت لایسنس MIT است.

## تماس و حمایت

در صورت داشتن سؤال یا مشکل، یک Issue باز کنید.
