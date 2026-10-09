from django.utils import timezone

from .models import CompanyValue, Inquiry, Metric, ProcessStep, Project, Service, SiteSettings, Testimonial


def new_inquiries_badge(request):
    return Inquiry.objects.filter(status="new").count()


def environment_callback(request):
    return ["تشغيل محلي", "success"]


def dashboard_callback(request, context):
    today = timezone.localdate()
    inquiries = Inquiry.objects.select_related("service")
    context.update(
        {
            "dashboard_site": SiteSettings.load(),
            "new_inquiries_count": inquiries.filter(status="new").count(),
            "today_inquiries_count": inquiries.filter(created_at__date=today).count(),
            "contacted_inquiries_count": inquiries.filter(status="contacted").count(),
            "closed_inquiries_count": inquiries.filter(status="closed").count(),
            "all_inquiries_count": inquiries.count(),
            "services_count": Service.objects.filter(is_active=True).count(),
            "projects_count": Project.objects.filter(is_active=True).count(),
            "testimonials_count": Testimonial.objects.filter(is_active=True).count(),
            "values_count": CompanyValue.objects.filter(is_active=True).count(),
            "steps_count": ProcessStep.objects.filter(is_active=True).count(),
            "metrics_count": Metric.objects.filter(is_active=True).count(),
            "recent_inquiries": inquiries[:7],
        }
    )
    return context
