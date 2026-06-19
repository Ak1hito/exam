from django.contrib import admin
from django.urls import include, path

from exam.views import home, ping


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("ping/", ping, name="ping"),
    path("", include("exam.urls")),
]
