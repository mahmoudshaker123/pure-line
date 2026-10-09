from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from website.admin import admin_site
from website.sitemaps import StaticViewSitemap
from website.views import robots


urlpatterns = [
    path("admin/", admin_site.urls),
    path("robots.txt", robots, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": {"static": StaticViewSitemap}}, name="sitemap"),
    path("", include("website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
