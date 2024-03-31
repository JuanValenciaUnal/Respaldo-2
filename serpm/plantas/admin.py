from django.contrib import admin

# Register your models here.
from .models import Afeciones,Generos,EnfermedadesAdicionales,Hipersensibilidad

# Register your models here.
admin.site.site_header="Panel de administración SERM"
admin.site.site_title="Panel de administración"
admin.site.index_title="Bienvenido(a)..."

class AfeccionesAdmin(admin.ModelAdmin):
    list_display =['id','afeccion','creado','modificado']#los campos que queremos mostrar
    search_fields=['afeccion'] # agregar campo de busquedas
    list_filter=['afeccion'] # para agregar filtros
    ordering=['afeccion'] # para ordenar descendente
    list_editable=['afeccion'] #OJONO PUEDE SER EL PRIMER CAMPO DE LA LISTA display
    list_per_page=30 # para listar por pagina x nuemro de registros

class GenerosAdmin(admin.ModelAdmin):
    list_display =['id','genero']#los campos que queremos mostrar
    search_fields=['genero'] # agregar campo de busquedas
    ordering=['genero'] # para ordenar descendente
    list_editable=['genero'] #OJONO PUEDE SER EL PRIMER CAMPO DE LA LISTA display
    list_per_page=30 # para listar por pagina x nuemro de registros

class EnfermedadesAdicionalesAdmin(admin.ModelAdmin):
    list_display =['id','enfermedad','creado','modificado']#los campos que queremos mostrar
    search_fields=['enfermedad'] # agregar campo de busquedas
    list_filter=['enfermedad'] # para agregar filtros
    ordering=['enfermedad'] # para ordenar descendente
    list_editable=['enfermedad'] #OJONO PUEDE SER EL PRIMER CAMPO DE LA LISTA display
    list_per_page=30 # para listar por pagina x nuemro de registros

class HipersensibilidadAdmin(admin.ModelAdmin):
    list_display =['id','componente','creado','modificado']#los campos que queremos mostrar
    search_fields=['componente'] # agregar campo de busquedas
    list_filter=['componente'] # para agregar filtros
    ordering=['componente'] # para ordenar descendente
    list_editable=['componente'] #OJONO PUEDE SER EL PRIMER CAMPO DE LA LISTA display
    list_per_page=30 # para listar por pagina x nuemro de registros


admin.site.register(Afeciones,AfeccionesAdmin)  
admin.site.register(Generos,GenerosAdmin) 
admin.site.register(EnfermedadesAdicionales,EnfermedadesAdicionalesAdmin) 
admin.site.register(Hipersensibilidad,HipersensibilidadAdmin)    