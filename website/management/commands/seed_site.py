from django.core.management.base import BaseCommand

from website.models import CompanyValue, Metric, ProcessStep, Project, Service, SiteSettings, Testimonial


SERVICES = [
    {
        "title": "المصاعد",
        "slug": "elevators",
        "short_description": "توريد وتركيب وصيانة المصاعد للمباني السكنية والتجارية بحلول تجمع الأمان والأناقة.",
        "description": "ننفذ أعمال المصاعد من دراسة البئر واختيار المواصفات حتى التركيب والتشغيل والصيانة الدورية.",
        "static_image": "images/projects/elevator-01.jpeg",
        "accent": "#d8a63a",
        "order": 1,
    },
    {
        "title": "المقاولات العامة",
        "slug": "general-contracting",
        "short_description": "بناء وتشطيب وترميم بإدارة تنفيذية توازن بين الجودة والبرنامج الزمني والتكلفة.",
        "description": "تنفيذ وإدارة الأعمال المدنية والمعمارية والتشطيبات للمشروعات السكنية والتجارية.",
        "static_image": "images/brand/brand-banner.jpeg",
        "accent": "#c8962e",
        "order": 2,
    },
    {
        "title": "السباكة والصرف",
        "slug": "plumbing-drainage",
        "short_description": "شبكات تغذية وصرف ومضخات وحلول متكاملة مصممة لتدفق آمن وتشغيل طويل الأمد.",
        "description": "توريد وتركيب واختبار شبكات المياه والصرف وخزانات ومضخات المباني مع عزل وتمديد منظم.",
        "static_image": "images/services/plumbing.webp",
        "accent": "#4fa3d1",
        "order": 3,
    },
    {
        "title": "الأعمال الكهربائية",
        "slug": "electrical",
        "short_description": "لوحات وقوى وإنارة وتمديدات تنفذ باحتراف وتختبر وفق متطلبات الأمان والكفاءة.",
        "description": "تنفيذ شبكات القوى والإنارة واللوحات والكابلات والتأريض والاختبارات والتشغيل.",
        "static_image": "images/services/electrical.webp",
        "accent": "#edb834",
        "order": 4,
    },
    {
        "title": "الحريق والإنذار",
        "slug": "fire-alarm",
        "short_description": "أنظمة مكافحة وإنذار مبكر تشمل الشبكات والمضخات والكواشف والاختبارات والصيانة.",
        "description": "تنفيذ وصيانة أنظمة الرش ومضخات الحريق والإنذار المبكر بما يرفع جاهزية المنشأة وسلامتها.",
        "static_image": "images/services/fire-system.jpg",
        "accent": "#d3483f",
        "order": 5,
    },
    {
        "title": "التكييف والتهوية",
        "slug": "hvac",
        "short_description": "تصميم وتركيب وصيانة أنظمة التكييف والتهوية لتحقيق راحة مستقرة وكفاءة أفضل للطاقة.",
        "description": "أعمال وحدات التكييف والدكت وخطوط النحاس والتهوية والاختبار والاتزان والصيانة الوقائية.",
        "static_image": "images/services/hvac.webp",
        "accent": "#7aa4b8",
        "order": 6,
    },
]

PROJECTS = [
    {
        "title": "تنفيذ شبكة مكافحة حريق متكاملة",
        "category": "الحريق والإنذار",
        "description": "شبكة رش ومواسير حريق منظمة داخل منشأة تجارية مع تنفيذ دقيق للمسارات والدعامات.",
        "static_image": "images/services/fire-system.jpg",
        "location": "المملكة العربية السعودية",
        "featured": True,
        "order": 1,
    },
    {
        "title": "تشطيب واجهة مصعد فاخرة",
        "category": "المصاعد",
        "description": "واجهة مصعد بتفاصيل زخرفية وتشطيب راق ينسجم مع الطابع الداخلي للمبنى.",
        "static_image": "images/projects/elevator-01.jpeg",
        "location": "خميس مشيط",
        "featured": False,
        "order": 2,
    },
    {
        "title": "منظومة لوحات وقوى كهربائية",
        "category": "الأعمال الكهربائية",
        "description": "لوحات توزيع ومسارات كابلات مرتبة مع اختبارات تشغيل وسلامة دقيقة.",
        "static_image": "images/services/electrical.webp",
        "location": "مكة المكرمة",
        "featured": False,
        "order": 3,
    },
    {
        "title": "منظومة تكييف وتهوية مركزية",
        "category": "التكييف والتهوية",
        "description": "وحدات مناولة هواء ودكت وخطوط تشغيل منفذة بما يرفع كفاءة الأداء وجودة الهواء.",
        "static_image": "images/services/hvac.webp",
        "location": "المملكة العربية السعودية",
        "featured": True,
        "order": 4,
    },
]

TESTIMONIALS = [
    {"name": "عميل قطاع سكني", "role": "مشروع مصاعد", "quote": "وضوح في مراحل العمل واهتمام بالتفاصيل من المعاينة وحتى التشغيل والتسليم.", "order": 1},
    {"name": "إدارة منشأة تجارية", "role": "أعمال كهروميكانيكية", "quote": "التنسيق بين الفرق الفنية وفر علينا الوقت وساعد على تسليم الأعمال بصورة منظمة.", "order": 2},
    {"name": "مالك مشروع", "role": "مقاولات وتشطيبات", "quote": "تواصل مباشر والتزام بالملاحظات وجودة واضحة في التشطيبات النهائية للمشروع.", "order": 3},
]

COMPANY_VALUES = [
    {"title": "الجودة", "description": "مواد معتمدة وتنفيذ يخضع للمراجعة في كل مرحلة.", "order": 1},
    {"title": "السلامة", "description": "إجراءات واضحة تحمي الموقع والفريق والمنشأة.", "order": 2},
    {"title": "الالتزام", "description": "جدول زمني واقعي وتواصل مباشر حتى التسليم.", "order": 3},
]

PROCESS_STEPS = [
    {"title": "المعاينة والدراسة", "description": "نفهم طبيعة الموقع ونراجع الاحتياج والمخططات ونحدد نطاق العمل بدقة.", "order": 1},
    {"title": "العرض والخطة", "description": "نقدّم تصورًا واضحًا للمواد والجدول الزمني وآلية التنفيذ والتكلفة.", "order": 2},
    {"title": "التنفيذ والرقابة", "description": "فريق متخصص ينفذ تحت إشراف هندسي مع فحوصات جودة وسلامة مستمرة.", "order": 3},
    {"title": "الاختبار والتسليم", "description": "نجري الاختبارات النهائية ونسلم الأعمال موثقة مع خيارات الصيانة والمتابعة.", "order": 4},
]

METRICS = [
    {"value": 6, "suffix": "", "label": "قطاعات هندسية متكاملة", "order": 1},
    {"value": 100, "suffix": "%", "label": "التزام بمعايير السلامة", "order": 2},
    {"value": 2, "suffix": "", "label": "مدن ضمن نطاق خدمتنا", "order": 3},
    {"value": 1, "suffix": "", "label": "فريق واحد لإدارة مشروعك", "order": 4},
]


class Command(BaseCommand):
    help = "إضافة المحتوى الافتراضي لموقع الخط النقي"

    def handle(self, *args, **options):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "hero_title": "نبني أنظمة تعمل. ونرفع معايير التنفيذ.",
                "hero_subtitle": "من المصاعد والمقاولات إلى السباكة والكهرباء وأنظمة الحريق والتكييف، نقدم إدارة هندسية متكاملة لمشروع أكثر أمانًا وكفاءة.",
                "about_title": "خبرة تنفيذية تجمع التفاصيل تحت سقف واحد",
                "about_text": "في الخط النقي ندير المشروع كمنظومة واحدة؛ ندرس الاحتياج، ننسق بين التخصصات، ننفذ وفق المواصفات، ثم نختبر ونسلم ونتابع. هدفنا أن يحصل العميل على جودة يمكن قياسها وثقة تستمر بعد انتهاء التنفيذ.",
            },
        )
        for data in SERVICES:
            Service.objects.update_or_create(slug=data["slug"], defaults=data)
        for data in PROJECTS:
            Project.objects.update_or_create(title=data["title"], defaults=data)
        for data in TESTIMONIALS:
            Testimonial.objects.update_or_create(name=data["name"], defaults=data)
        for data in COMPANY_VALUES:
            CompanyValue.objects.update_or_create(title=data["title"], defaults=data)
        for data in PROCESS_STEPS:
            ProcessStep.objects.update_or_create(title=data["title"], defaults=data)
        for data in METRICS:
            Metric.objects.update_or_create(label=data["label"], defaults=data)
        self.stdout.write(self.style.SUCCESS("Pure Line site content is ready."))
