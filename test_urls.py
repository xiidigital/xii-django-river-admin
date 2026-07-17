from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include("xii.django_river_admin.urls")),
    re_path(r'^api-auth/', include('rest_framework.urls')),
]
