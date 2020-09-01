from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("wydatki/", include("expense.urls")),
    path("", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("price_scraper.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
