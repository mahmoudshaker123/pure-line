from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Inquiry, Service, SiteSettings


class WebsiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSettings.objects.create(
            hero_title="عنوان تجريبي",
            hero_subtitle="وصف تجريبي",
            about_title="من نحن",
            about_text="نبذة تجريبية",
        )
        cls.service = Service.objects.create(
            title="الكهرباء",
            slug="electricity",
            short_description="وصف مختصر",
            description="التفاصيل",
        )
        cls.admin_user = get_user_model().objects.create_superuser(
            username="test-admin",
            email="admin@example.com",
            password="StrongTestPassword123!",
        )

    def test_home_page_renders_dynamic_content(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "عنوان تجريبي")
        self.assertContains(response, "الكهرباء")
        self.assertContains(response, '"@type": "LocalBusiness"')

    def test_valid_inquiry_is_saved(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "عميل تجريبي",
                "phone": "0500000000",
                "email": "client@example.com",
                "service": self.service.pk,
                "location": "خميس مشيط",
                "message": "أرغب في معاينة المشروع وتقديم عرض سعر.",
            },
        )
        self.assertRedirects(response, f"{reverse('home')}#contact", fetch_redirect_response=False)
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_honeypot_rejects_bot_submission(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Bot",
                "phone": "0500000000",
                "message": "Spam message",
                "website": "https://spam.invalid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_health_check(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_robots_and_sitemap(self):
        robots_response = self.client.get(reverse("robots"))
        self.assertContains(robots_response, "Disallow: /admin/")
        sitemap_response = self.client.get(reverse("sitemap"))
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, "<loc>http://testserver/</loc>")

    def test_uploaded_service_image_is_optimized_to_webp(self):
        from PIL import Image

        source = BytesIO()
        Image.new("RGB", (2200, 1400), "#d8a63a").save(source, format="PNG")
        service = Service.objects.create(
            title="خدمة بصورة",
            slug="optimized-image",
            short_description="وصف",
            description="تفاصيل",
            image=SimpleUploadedFile("large.png", source.getvalue(), content_type="image/png"),
        )
        try:
            self.assertTrue(service.image.name.endswith(".webp"))
            with Image.open(service.image.path) as optimized:
                self.assertLessEqual(optimized.width, 1600)
                self.assertLessEqual(optimized.height, 1200)
        finally:
            service.image.delete(save=False)

    def test_invalid_inquiry_returns_errors(self):
        response = self.client.post(reverse("home"), {"name": "عميل"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "راجع البيانات المطلوبة")
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_admin_dashboard_renders_for_staff(self):
        self.client.force_login(self.admin_user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "أحدث طلبات التواصل")
        self.assertContains(response, "إعدادات الشركة")

    def test_company_contact_details_are_dynamic(self):
        settings = SiteSettings.objects.get()
        settings.phone_primary = "0555555555"
        settings.email = "new@example.com"
        settings.contact_title = "عنوان تواصل قابل للتعديل"
        settings.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "0555555555")
        self.assertContains(response, "new@example.com")
        self.assertContains(response, "عنوان تواصل قابل للتعديل")

    def test_admin_content_pages_render(self):
        self.client.force_login(self.admin_user)
        for url in (
            "/admin/website/sitesettings/",
            "/admin/website/service/",
            "/admin/website/project/",
            "/admin/website/inquiry/",
            "/admin/website/processstep/",
            "/admin/website/companyvalue/",
            "/admin/website/metric/",
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
