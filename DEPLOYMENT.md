# نشر النسخة Static على Cloudflare Pages

النسخة الحالية أصبحت Static بالكامل: لا تحتاج Django أو PostgreSQL أو Docker أو VPS. تحتاج فقط إلى الدومين، وCloudflare Pages المجاني لاستضافة ملفات HTML/CSS/JS والصور.

## الملفات المهمة

- `index.html`: الصفحة الرئيسية الجاهزة.
- `assets/`: CSS وJavaScript والصور المضغوطة.
- `404.html`: صفحة الخطأ.
- `_headers`: كاش وحماية للملفات.

نموذج التواصل لا يحتاج قاعدة بيانات؛ عند الإرسال يفتح واتساب برسالة جاهزة على رقم الشركة. عدّل الرقم داخل `assets/js/site.js` إذا تغير رقم الواتساب.

## النشر

1. اشترِ الدومين، ثم أضفه إلى حساب Cloudflare.
2. في Cloudflare Dashboard افتح **Workers & Pages → Create application → Pages → Import existing Git repository**.
3. اختر مستودع `pure-line` وفرع `main`.
4. اجعل Build command فارغًا أو `exit 0`، وBuild output directory هو `/` أو اتركه الافتراضي إذا كان الجذر هو المشروع.
5. بعد النشر أضف `purelineksa.com` و`www.purelineksa.com` من Custom domains. Cloudflare ينشئ HTTPS تلقائيًا.

## تحديث الموقع

عدّل `index.html` أو ملفات `assets/`، ثم:

```bash
git add .
git commit -m "Update profile content"
git push origin main
```

Cloudflare Pages سيعيد النشر تلقائيًا بعد كل Push.

## ملاحظات مهمة

- لا توجد لوحة إدارة في النسخة Static. تعديل النصوص والصور يتم من ملفات المشروع ثم Push.
- لا توجد قاعدة بيانات أو طلبات محفوظة؛ طلبات التواصل تصل عبر واتساب.
- لا تضع كلمات سر أو مفاتيح API داخل JavaScript.
- استضافة Pages مجانية، لكن تجديد الدومين يظل التكلفة السنوية الوحيدة.
