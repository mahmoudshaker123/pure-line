import logging

from django.conf import settings as django_settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import InquiryForm
from .models import CompanyValue, Metric, ProcessStep, Project, Service, SiteSettings, Testimonial


logger = logging.getLogger(__name__)


def robots(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(
        f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {sitemap_url}\n",
        content_type="text/plain; charset=utf-8",
    )


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        logger.exception("Database health check failed")
        return JsonResponse({"status": "unhealthy"}, status=503)
    return JsonResponse({"status": "ok"})


def home(request):
    settings = SiteSettings.load()
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            if django_settings.CONTACT_NOTIFICATION_EMAIL:
                try:
                    send_mail(
                        subject=f"طلب جديد من الموقع: {inquiry.name}",
                        message=(
                            f"الاسم: {inquiry.name}\nالهاتف: {inquiry.phone}\n"
                            f"البريد: {inquiry.email or '-'}\nالخدمة: {inquiry.service or '-'}\n"
                            f"الموقع: {inquiry.location or '-'}\n\n{inquiry.message}"
                        ),
                        from_email=django_settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[django_settings.CONTACT_NOTIFICATION_EMAIL],
                    )
                except Exception:
                    logger.exception("Could not send inquiry notification email")
            messages.success(request, f"شكرًا {inquiry.name}، استلمنا طلبك وسيتواصل معك فريقنا قريبًا.")
            return redirect(f"{reverse('home')}#contact")
        messages.error(request, "راجع البيانات المطلوبة ثم حاول مرة أخرى.")
    else:
        form = InquiryForm()

    context = {
        "site": settings,
        "services": Service.objects.filter(is_active=True),
        "projects": Project.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
        "company_values": CompanyValue.objects.filter(is_active=True),
        "process_steps": ProcessStep.objects.filter(is_active=True),
        "metrics": Metric.objects.filter(is_active=True),
        "form": form,
    }
    return render(request, "website/home.html", context)
