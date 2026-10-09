# نشر موقع الخط النقي على Production

التجهيز الحالي يستخدم Docker Compose ويشغّل أربعة أجزاء مترابطة: Django عبر Gunicorn، قاعدة PostgreSQL، وخادم Caddy الذي يفعّل HTTPS ويضغط الاستجابات تلقائيًا. الصور المرفوعة من لوحة الإدارة وقاعدة البيانات محفوظتان في Docker volumes دائمة.

## المشتريات المطلوبة

1. دومين واحد، ويفضل اسم `.com` قصيرًا وواضحًا. استخدم `.sa` فقط إذا كان مهمًا للهوية المحلية ومستندات التسجيل متاحة.
2. VPS بنظام Ubuntu LTS، بمواصفات 2 vCPU وذاكرة 4GB وقرص SSD لا يقل عن 40GB. هذه المواصفات كافية جدًا للموقع في بدايته.
3. تفعيل النسخ الاحتياطي التلقائي لدى شركة السيرفر إن كان سعره مناسبًا.
4. حساب Cloudflare مجاني لإدارة DNS والحماية وCDN؛ لا تحتاج شراء SSL أو CDN مدفوع.
5. اختياري: بريد باسم الدومين وخدمة SMTP لإرسال إشعار عند وصول طلب عميل. الموقع سيحفظ الطلبات في لوحة الإدارة حتى دون SMTP.

لا تحتاج حاليًا إلى قاعدة بيانات Managed مدفوعة، أو لوحة cPanel، أو استضافة صور مستقلة.

## 1. تجهيز السيرفر

- أنشئ VPS بـ Ubuntu LTS وسجّل الدخول بمفتاح SSH، وليس بكلمة مرور فقط.
- حدّث النظام وثبّت Docker Engine وDocker Compose plugin من تعليمات Docker الرسمية.
- فعّل جدار الحماية وافتح المنافذ `22`, `80`, `443` فقط.
- أنشئ مستخدمًا عاديًا بصلاحية sudo لتشغيل المشروع، ولا تستخدم root في العمل اليومي.

مثال لمجلد المشروع:

```bash
sudo mkdir -p /opt/pure-line
sudo chown "$USER":"$USER" /opt/pure-line
git clone https://github.com/mahmoudshaker123/pure-line.git /opt/pure-line
cd /opt/pure-line
```

## 2. إعداد الدومين

في Cloudflare DNS أضف السجلين التاليين إلى IP السيرفر:

- `A` للاسم `@`
- `A` للاسم `www`

في أول تشغيل يمكن إبقاء Proxy في وضع DNS only. بعد التأكد من أن HTTPS يعمل، فعّل Proxy البرتقالي إن أردت CDN وحماية إضافية، واجعل SSL/TLS في Cloudflare على `Full (strict)`.

## 3. أسرار وإعدادات Production

```bash
cd /opt/pure-line
cp .env.production.example .env.production
chmod 600 .env.production
openssl rand -base64 48
openssl rand -base64 36
nano .env.production
```

- ضع الدومين من دون `https://` في `DOMAIN`.
- استخدم الناتج الأول في `DJANGO_SECRET_KEY` والثاني في `POSTGRES_PASSWORD`.
- لا ترفع ملف `.env.production` إلى Git.
- إعدادات SMTP في آخر الملف اختيارية، ويمكن إضافتها لاحقًا.

## 4. التشغيل لأول مرة

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.production -f docker-compose.prod.yml exec web python manage.py seed_site
docker compose --env-file .env.production -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker compose --env-file .env.production -f docker-compose.prod.yml ps
```

شغّل `seed_site` مرة واحدة فقط على قاعدة جديدة؛ إعادة تشغيله لاحقًا قد تعيد بعض المحتوى الافتراضي فوق تعديلات لوحة الإدارة.

افتح بعدها:

- الموقع: `https://YOUR-DOMAIN/`
- لوحة الإدارة: `https://YOUR-DOMAIN/admin/`
- فحص الخدمة: `https://YOUR-DOMAIN/health/`

## نقل محتوى النسخة المحلية بدل المحتوى الافتراضي

إذا عدّلت المحتوى محليًا وتريد نفس البيانات على السيرفر، صدّرها قبل الرفع:

```powershell
.\.venv\Scripts\python.exe manage.py dumpdata website --indent 2 -o site-data.json
```

انسخ `site-data.json` وأي ملفات داخل `media/` إلى السيرفر، ثم بعد أول تشغيل والمهاجرات:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml cp site-data.json web:/tmp/site-data.json
docker compose --env-file .env.production -f docker-compose.prod.yml exec web python manage.py loaddata /tmp/site-data.json
docker run --rm -v pureline_media_data:/target -v "$PWD/media:/source:ro" alpine sh -c 'cp -a /source/. /target/'
```

لا تشغّل `seed_site` في هذه الحالة. أنشئ مستخدم الإدارة على السيرفر باستخدام `createsuperuser` ولا تنقل كلمة مرور الإدارة التجريبية.

## النسخ الاحتياطي

اجعل السكربت قابلًا للتشغيل ثم اختبره:

```bash
chmod +x scripts/backup.sh
./scripts/backup.sh
```

لتشغيل نسخة يومية الساعة 3 صباحًا:

```cron
0 3 * * * cd /opt/pure-line && ./scripts/backup.sh >> /var/log/pureline-backup.log 2>&1
```

السكربت يحتفظ بآخر 14 يومًا من قاعدة البيانات والصور المرفوعة. يجب أيضًا نسخ مجلد `backups/` إلى مكان خارج نفس السيرفر أو تفعيل Backups/Snapshots لدى مزود الـ VPS؛ وجود النسخة على نفس السيرفر وحده غير كافٍ.

## التحديثات اللاحقة

```bash
cd /opt/pure-line
git pull --ff-only
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker image prune -f
```

الـ container ينفذ `migrate` و`collectstatic` تلقائيًا قبل تشغيل Gunicorn. راقب السجلات بعد كل تحديث:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml logs --tail=150 web caddy
```

## فحص ما قبل التسليم

- غيّر كلمة مرور الإدارة المحلية ولا تستخدمها على Production.
- اختبر إرسال نموذج التواصل وظهور الطلب داخل لوحة الإدارة.
- عدّل الهاتف والبريد والعنوان وروابط التواصل وSEO من إعدادات الشركة في لوحة الإدارة.
- راجع الموقع على الهاتف والكمبيوتر.
- تأكد من `https://` ومن تحويل `www` إلى الدومين الرئيسي.
- اختبر استعادة Backup مرة واحدة، وليس إنشاءه فقط.
- اربط Google Search Console وGoogle Analytics أو أداة تحليلات تحترم الخصوصية إذا احتجت قياس الزيارات.
