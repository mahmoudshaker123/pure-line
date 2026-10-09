from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.sites import UnfoldAdminSite

from .models import (
    CompanyValue,
    Inquiry,
    Metric,
    ProcessStep,
    Project,
    Service,
    SiteSettings,
    Testimonial,
)


class PureLineAdminSite(UnfoldAdminSite):
    site_header = "الخط النقي | لوحة الإدارة"
    site_title = "إدارة الخط النقي"
    index_title = "مرحبًا بك في مركز إدارة الموقع"
    index_template = "admin/pureline_index.html"


admin_site = PureLineAdminSite(name="pureline_admin")


class OrderedAdmin(ModelAdmin):
    list_display = ("title", "visible_status", "order")
    list_editable = ("order",)
    list_filter = ("is_active",)
    ordering = ("order", "id")
    warn_unsaved_form = True

    @display(description="الحالة", label={"ظاهر": "success", "مخفي": "danger"})
    def visible_status(self, obj):
        return "ظاهر" if obj.is_active else "مخفي"


class ServiceAdmin(OrderedAdmin):
    list_display = ("title", "visible_status", "order", "image_preview")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("بيانات الخدمة", {"fields": ("title", "slug", "short_description", "description")}),
        ("الصورة والهوية", {"fields": ("image", "static_image", "accent")}),
        ("الظهور والترتيب", {"fields": ("is_active", "order")}),
    )

    @display(description="الصورة")
    def image_preview(self, obj):
        return format_html('<img src="{}" style="width:52px;height:38px;object-fit:cover;border-radius:8px">', obj.image_url) if obj.image_url else "-"


class ProjectAdmin(OrderedAdmin):
    list_display = ("title", "category", "location", "featured", "visible_status", "order")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("title", "description", "location")
    fieldsets = (
        ("المشروع", {"fields": ("title", "category", "description", "location")}),
        ("الصورة", {"fields": ("image", "static_image")}),
        ("العرض", {"fields": ("featured", "is_active", "order")}),
    )


class TestimonialAdmin(OrderedAdmin):
    list_display = ("name", "role", "visible_status", "order")
    search_fields = ("name", "role", "quote")

    @display(description="الاسم")
    def title(self, obj):
        return obj.name


class CompanyValueAdmin(OrderedAdmin):
    search_fields = ("title", "description")


class ProcessStepAdmin(OrderedAdmin):
    search_fields = ("title", "description")


class MetricAdmin(OrderedAdmin):
    list_display = ("metric_value", "label", "visible_status", "order")
    search_fields = ("label",)

    @display(description="الرقم", ordering="value")
    def metric_value(self, obj):
        return f"{obj.value}{obj.suffix}"

    @display(description="العنوان")
    def title(self, obj):
        return obj.label


class InquiryAdmin(ModelAdmin):
    list_display = ("customer", "phone", "service", "location", "status_badge", "created_at")
    list_filter = ("status", "service", "created_at")
    search_fields = ("name", "phone", "email", "message", "location")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = ("mark_contacted", "mark_closed", "mark_new")
    fieldsets = (
        ("بيانات العميل", {"fields": (("name", "phone"), ("email", "location"))}),
        ("تفاصيل الطلب", {"fields": ("service", "message")}),
        ("المتابعة", {"fields": ("status", "created_at")}),
    )

    @display(description="العميل", ordering="name", header=True)
    def customer(self, obj):
        return obj.name, obj.email or "بدون بريد", obj.name[:1]

    @display(description="الحالة", ordering="status", label={"جديد": "warning", "تم التواصل": "info", "مغلق": "success"})
    def status_badge(self, obj):
        return obj.get_status_display()

    @admin.action(description="تحديد الطلبات: تم التواصل")
    def mark_contacted(self, request, queryset):
        count = queryset.update(status="contacted")
        self.message_user(request, f"تم تحديث {count} طلب.", messages.SUCCESS)

    @admin.action(description="تحديد الطلبات: مغلقة")
    def mark_closed(self, request, queryset):
        count = queryset.update(status="closed")
        self.message_user(request, f"تم إغلاق {count} طلب.", messages.SUCCESS)

    @admin.action(description="إعادة الطلبات إلى: جديد")
    def mark_new(self, request, queryset):
        count = queryset.update(status="new")
        self.message_user(request, f"تمت إعادة {count} طلب إلى جديد.", messages.SUCCESS)


class SiteSettingsAdmin(ModelAdmin):
    list_display = ("company_name", "phone_primary", "email", "edit_hint")
    warn_unsaved_form = True
    save_on_top = True
    readonly_fields = ("logo_preview", "hero_preview")
    fieldsets = (
        ("هوية الشركة", {"fields": ("company_name", "company_name_en", "commercial_registration", ("logo", "logo_preview"))}),
        ("الواجهة الرئيسية", {"fields": ("hero_title", "hero_subtitle", ("hero_image", "hero_preview"))}),
        ("قسم من نحن", {"fields": ("about_title", "about_text")}),
        ("قسم التواصل والفوتر", {"fields": ("contact_title", "contact_text", "footer_text")}),
        ("أرقام وبيانات التواصل", {"fields": (("phone_primary", "phone_secondary"), "whatsapp", ("email", "sales_email"), "address", "business_hours", "google_maps_url")}),
        ("روابط التواصل الاجتماعي", {"fields": (("instagram_url", "x_url"), ("linkedin_url", "tiktok_url"), "snapchat_url"), "classes": ("collapse",)}),
        ("محركات البحث SEO", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )

    @display(description="الحالة", label={"جاهز للتعديل": "success"})
    def edit_hint(self, obj):
        return "جاهز للتعديل"

    @display(description="الشعار الحالي")
    def logo_preview(self, obj):
        return format_html('<img src="{}" style="width:100px;height:100px;object-fit:cover;border-radius:16px">', obj.logo_url)

    @display(description="صورة الواجهة الحالية")
    def hero_preview(self, obj):
        return format_html('<img src="{}" style="width:260px;height:150px;object-fit:cover;border-radius:16px">', obj.hero_image_url)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin_site.register(Service, ServiceAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(Testimonial, TestimonialAdmin)
admin_site.register(CompanyValue, CompanyValueAdmin)
admin_site.register(ProcessStep, ProcessStepAdmin)
admin_site.register(Metric, MetricAdmin)
admin_site.register(Inquiry, InquiryAdmin)
admin_site.register(SiteSettings, SiteSettingsAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
