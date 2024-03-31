from django.urls import path
from django.conf import settings
from . import views

# ********************************
# importacionespara las rutas de las imagenes
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),  
    path('acercade/',views.acercadeV,name='acercade'),  
    path('cargadatos/',views.cargadatosV,name='cargadatos'),  
    path('recomendaciones/',views.recomendacionesV,name='recomendaciones'),

    
   
]
