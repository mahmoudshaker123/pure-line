from django.core.validators import RegexValidator
from django.db import models

from .image_utils import optimize_uploaded_image


class OrderedActiveModel(models.Model):
    is_active = models.BooleanField("ظاهر في الموقع", default=True)
    order = models.PositiveIntegerField("الترتيب", default=0)

    class Meta:
        abstract = True
        ordering = ("order", "id")


class SiteSettings(models.Model):
    company_name = models.CharField("اسم الشركة", max_length=180, default="مؤسسة الخط النقي للمقاولات والمصاعد")
    company_name_en = models.CharField("الاسم بالإنجليزية", max_length=180, default="Pure Line for Contracting and Elevators Est.")
    logo = models.ImageField("شعار الشركة", upload_to="brand/", blank=True, help_text="اتركه فارغًا لاستخدام الشعار الحالي.")
    hero_image = models.ImageField("صورة الواجهة الرئيسية", upload_to="brand/", blank=True, help_text="اتركها فارغة لاستخدام صورة التكييف الحالية.")
    hero_title = models.CharField("عنوان الواجهة", max_length=220)
    hero_subtitle = models.TextField("وصف الواجهة")
    about_title = models.CharField("عنوان من نحن", max_length=220)
    about_text = models.TextField("نبذة عن الشركة")
    contact_title = models.CharField("عنوان قسم التواصل", max_length=220, default="فكرتك جاهزة لتتحول إلى واقع؟")
    contact_text = models.TextField("نص قسم التواصل", default="أرسل تفاصيلك وسيقوم فريقنا بمراجعتها والتواصل معك لتحديد الخطوة الأنسب.")
    footer_text = models.CharField("نص أسفل الموقع", max_length=300, default="حلول المقاولات والمصاعد والأعمال الكهروميكانيكية بمعيار واحد من الجودة.")
    phone_primary = models.CharField("الهاتف الأول", max_length=20, default="0534201283")
    phone_secondary = models.CharField("الهاتف الثاني", max_length=20, default="0506019745", blank=True)
    whatsapp = models.CharField("رقم واتساب بالصيغة الدولية", max_length=20, default="966534201283")
    email = models.EmailField("البريد الإلكتروني", default="info@pureline.sa")
    sales_email = models.EmailField("بريد المبيعات", blank=True)
    address = models.CharField("العنوان", max_length=250, default="المملكة العربية السعودية - خميس مشيط ومكة المكرمة")
    business_hours = models.CharField("ساعات العمل", max_length=160, default="السبت - الخميس: 8 صباحًا حتى 6 مساءً", blank=True)
    google_maps_url = models.URLField("رابط الموقع على Google Maps", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    x_url = models.URLField("X / Twitter", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    tiktok_url = models.URLField("TikTok", blank=True)
    snapchat_url = models.URLField("Snapchat", blank=True)
    commercial_registration = models.CharField("السجل التجاري", max_length=40, default="4031303184")
    meta_title = models.CharField("عنوان محركات البحث", max_length=180, blank=True)
    meta_description = models.CharField("وصف محركات البحث", max_length=300, blank=True)

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        optimize_uploaded_image(self, "logo", max_size=(800, 800))
        optimize_uploaded_image(self, "hero_image")
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.first() or cls()

    @property
    def logo_url(self):
        return self.logo.url if self.logo else "/static/images/brand/logo-v2.webp"

    @property
    def hero_image_url(self):
        return self.hero_image.url if self.hero_image else "/static/images/services/hvac.webp"


class Service(OrderedActiveModel):
    title = models.CharField("اسم الخدمة", max_length=120)
    slug = models.SlugField("الرابط المختصر", unique=True, allow_unicode=True)
    short_description = models.CharField("الوصف المختصر", max_length=260)
    description = models.TextField("التفاصيل")
    image = models.ImageField("الصورة", upload_to="services/", blank=True)
    static_image = models.CharField("مسار صورة افتراضية", max_length=180, blank=True)
    accent = models.CharField("لون البطاقة", max_length=20, default="#d8a63a")

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        optimize_uploaded_image(self, "image")
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"/static/{self.static_image}" if self.static_image else ""


class Project(OrderedActiveModel):
    title = models.CharField("اسم المشروع", max_length=160)
    category = models.CharField("التصنيف", max_length=100)
    description = models.TextField("وصف المشروع")
    image = models.ImageField("الصورة", upload_to="projects/", blank=True)
    static_image = models.CharField("مسار صورة افتراضية", max_length=180, blank=True)
    location = models.CharField("الموقع", max_length=120, blank=True)
    featured = models.BooleanField("مشروع مميز", default=False)

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "مشروع"
        verbose_name_plural = "المشروعات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        optimize_uploaded_image(self, "image")
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"/static/{self.static_image}" if self.static_image else ""


class Testimonial(OrderedActiveModel):
    name = models.CharField("الاسم", max_length=100)
    role = models.CharField("الصفة أو القطاع", max_length=120, blank=True)
    quote = models.TextField("الرأي")

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "رأي عميل"
        verbose_name_plural = "آراء العملاء"

    def __str__(self):
        return self.name


class CompanyValue(OrderedActiveModel):
    title = models.CharField("القيمة", max_length=80)
    description = models.CharField("الوصف", max_length=240)

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "قيمة الشركة"
        verbose_name_plural = "قيم الشركة"

    def __str__(self):
        return self.title


class ProcessStep(OrderedActiveModel):
    title = models.CharField("عنوان الخطوة", max_length=120)
    description = models.CharField("الوصف", max_length=300)

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "خطوة عمل"
        verbose_name_plural = "خطوات العمل"

    def __str__(self):
        return self.title


class Metric(OrderedActiveModel):
    value = models.PositiveIntegerField("الرقم")
    suffix = models.CharField("اللاحقة", max_length=12, blank=True, help_text="مثال: % أو +")
    label = models.CharField("الوصف", max_length=120)

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "رقم وإحصائية"
        verbose_name_plural = "الأرقام والإحصائيات"

    def __str__(self):
        return f"{self.value}{self.suffix} - {self.label}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("new", "جديد"),
        ("contacted", "تم التواصل"),
        ("closed", "مغلق"),
    ]
    phone_validator = RegexValidator(r"^[0-9+() -]{8,20}$", "أدخل رقم هاتف صحيحًا.")

    name = models.CharField("الاسم", max_length=100)
    phone = models.CharField("رقم الجوال", max_length=20, validators=[phone_validator])
    email = models.EmailField("البريد الإلكتروني", blank=True)
    service = models.ForeignKey(Service, verbose_name="الخدمة", on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField("المدينة / الموقع", max_length=120, blank=True)
    message = models.TextField("تفاصيل الطلب")
    status = models.CharField("الحالة", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("تاريخ الطلب", auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "طلب تواصل"
        verbose_name_plural = "طلبات التواصل"

    def __str__(self):
        return f"{self.name} - {self.phone}"
