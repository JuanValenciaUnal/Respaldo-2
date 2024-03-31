from django.contrib import admin
from django.urls import path,include

# importacionespara las rutas de las imagenes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('plantas.urls')),
]