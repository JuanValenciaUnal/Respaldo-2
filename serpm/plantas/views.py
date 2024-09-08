from experta import *
import pandas as pd
#importaciones para recaptcha
import urllib
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

# Para usar librerias que ya ecxisten:
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
# manejo de autenticaciones
from django.contrib.auth import login,logout,authenticate

# para validar que el ussuario este logueado
from django.contrib.auth.decorators import login_required

# Mensajeria
from django.contrib import messages

#paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from .forms import ProductosGastronomiaF
from .models import Afeciones,Generos,EnfermedadesAdicionales,Hipersensibilidad

#Definicion vector de respuestas
global hipsesensibilidades
plantas_recomendadas= []
# Create your views here.
# **********************************
def home(request):
    # cuando se llama por primera vez carga todos los productos
    if request.method=='GET':
        #pro= Plantasventa.objects.all()
        afecciones= Afeciones.objects.all().order_by('creado').values('id','afeccion')
        generos= Generos.objects.all().order_by('creado').values('id','genero')
        enferemdadesadicionales=EnfermedadesAdicionales.objects.all()
        hipersensibilidades=Hipersensibilidad.objects.all()
        nr=afecciones.count()
        return render(request, 'home.html',{'afecciones':afecciones,'generos':generos,'enferemdadesadicionales':enferemdadesadicionales,'hipersensibilidades':hipersensibilidades,'nr':nr})   
    # cuando se llama desde la caja buscar de mismo listado

def recomendacionesV(request):
    
    #print(request.POST)
    afeccionv=str(request.POST.get('afecciones'))
    edadv=int(request.POST.get('edad'))
    generov=str(request.POST.get('genero'))
    embarazov=str(request.POST.get('embarazo'))
    lactanciav=str(request.POST.get('lactancia'))
    
    #Estas son de seelcion multiple
    enfermedadesadicinales = list(request.POST.getlist('enfermedadesa'))
    #Se obtiene dada elemento de x poosiciones
    for enfermedad in enfermedadesadicinales:
        print(enfermedad)

    # elemento de x poosiciones y los pasa a minusculas
    hipsesensibilidades = [valor.lower() for valor in request.POST.getlist('hipsesensibilidades')]
    for hipersensibilidad in hipsesensibilidades:
        print(hipersensibilidad)

    plantas_recomendadas.clear()
    engine =Base_de_conocimiento()
    engine.reset()
    engine.declare(SistemaAfectado(afectacion=afeccionv),embarazo(estado=embarazov),lactancia(estado=lactanciav),edad(x=edadv))
    engine.run()


    return render(request, 'recomendaciones.html',{'plantas_recomendadas':plantas_recomendadas})


#***************************************
def acercadeV(request):
    return render(request, 'acercade.html')
#****************************************

def cargadatosV(request):
    genero=request.GET.get('genero')
    if genero=='Masculino':
        return render(request, 'estadosh.html')  
    else:
        return render(request, 'estadosm.html')  




#Hecho1
class SistemaAfectado(Fact):
    #Informacion sobre el sistema afectado por la enfermedad del
    pass

class embarazo(Fact):
    #La persona se encuentra en estado de embarazo o no
    pass

class lactancia(Fact):
    #La persona se encuentra en estado de lactancia o no
    pass

class edad(Fact):
    #Edad de la persona
    pass

class enfermedades_adicionales(Fact):
    #Enfermedades adicionales que pueda tener una persona y que afecten el diacnostico
    pass

class hipersensibilidad(Fact):
    #hipersensibilidades a algun compuesto de alguna planta
    pass


def buscar_valores(dataframe, lista_busqueda):
    resultados = []
    for valor in lista_busqueda:
        # Buscar si el valor está en cualquier parte de la columna 7
        mask = dataframe.iloc[:, 6].str.contains(valor, case=False, na=False)
        # Filtrar el DataFrame usando la máscara de la planta
        resultados.extend(dataframe.loc[mask, 'Planta '].tolist())
        #Elimino duplicados
        sin_duplicados = set(resultados)

class Base_de_conocimiento(KnowledgeEngine):
    
#Reglas principales primer nivel
    #Tratamiento golpes o heridas
    @Rule(SistemaAfectado(afectacion='Golpes o heridas'))
    def IdentificarAfectacion(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'))
    #Tratamiento problemas cardiovasculares
    @Rule(SistemaAfectado(afectacion='Problemas cardiovasculares'))
    def IdentificarAfectacion2(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'))
    #Tratamiento problemas respiratorios
    @Rule(SistemaAfectado(afectacion='Problemas respiratorios'))
    def IdentificarAfectacion3(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades respiratorias'))
    #Tratamiento problemas Digestivos
    @Rule(SistemaAfectado(afectacion='Problemas digestivos'))
    def IdentificarAfectacion4(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades digestivas'))
    #Tratamiento problemas inmunologicos
    @Rule(SistemaAfectado(afectacion='Problemas inmunologicos'))
    def IdentificarAfectacion5(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'))  
    #Tratamiento problemas gastrointestinales
    @Rule(SistemaAfectado(afectacion='Problemas gastrointestinales'))
    def IdentificarAfectacion6(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'))
    #Tratamiento problemas Dermatologicos o cicatrizantes
    @Rule(SistemaAfectado(afectacion='Problemas dermatologicos o cicatrizantes'))
    def IdentificarAfectacion7(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'))
    #Tratamiento problemas reproductivos y hormonales
    @Rule(SistemaAfectado(afectacion='Problemas reproductivos y hormonales'))
    def IdentificarAfectacion8(self):
        plantas_recomendadas = []
        self.declare(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'))        
        
#Reglas segundo nivel
    #AA para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion(self): 
        plantas_recomendadas.extend(['Ortiga','Verbena','Guarana','Sangre de drago','Balsamina','Culantro','Canela','Cidron','Limoncillo','Menta','Pasiflora','Mielenrama'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
    #AA para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion2(self):
        plantas_recomendadas.extend(['Achiote','Guaba','Aji','Arnica','Canelo de monte','Pronto alivio','Sauce','Guaba','Trigo sarraceno'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

     #Cardiovasculares para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion3(self): 
        plantas_recomendadas.extend(['Guarana','Ortiga','Vid','Ginseng'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

     #Cardiovasculares para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion4(self):
        plantas_recomendadas.extend(['Cafe','Ginkgo biloba','Yarumo','Ajo','Trigo sarraceno'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
    
    #Respiratorias para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades respiratorias'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion5(self):
        plantas_recomendadas.extend(['Eucalipto','Ginseng','Hiedra','Hisopo','Jengibre','Malva','Oregano','Pensamiento','Sabila','Sauco','Verbena','Vira-vira','Cimifuga','Ruda','Violeta','Mielenrama','Guarana','Canela','Quina','Salvia'])
        self.declare(edad(evaluacion='y'))
        self.declare(enfermedades_adicionales(evaluacion='y'))
        

    #Respiratorias para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades respiratorias'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion6(self):
        plantas_recomendadas.extend(['Marrubio blanco','Pronto alivio','Algarrobo','Arnica'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
        
    #Digestivas no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades digestivas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion7(self):
        plantas_recomendadas.extend(['Ajenjo','Cardamomo','Genciana','Mielenrama','Romero','Canela','Cimicifuga','Culantro','Gienseng','Oregano','Salvia'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

    #Digestivas embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades digestivas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion8(self):
        plantas_recomendadas.extend(['Rabano','Marrubio','Sauce','Pronto alivio','Toronjil','Valeriana','Zanahoria'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
        
    #Inunologicas no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion9(self):  
        plantas_recomendadas.extend(['Geranio','Onagra','Verbena littoralis','Balsamina','Ruda','Salvia','Ajenjo','Anamu','Eucalipto'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

    #Inunologicas embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion10(self):
        plantas_recomendadas.extend(['Ginkgo biloba','Trigo sarraceno','Equinacea','Ajo','Casco de vaca','Zanahoria','Rabano'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
    
    #gastrointestinales no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion11(self):   
        plantas_recomendadas.extend(['Boldo','Cascara sagrada','Ispagula','Malva','Manzanilla','Psyllium','Ruibardo','Sabila','Sauco','Sen','Balsamina','Cimicifuga','Quina','Albahaca','Limoncillo','Menta','Oregano','Perejil','Salvia','Yerbabuena'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

    #gastrointestinales embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion12(self):
        plantas_recomendadas.extend(['Higuerilla','Linaza','Papaya','Casco de vaca','Chilca','Nogal blanco','Anis','Cidron','Eneldo'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))
       
    #dermatologica y cicatrizantes no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion13(self):
        plantas_recomendadas.extend(['Anamu','Balsamina','Boton negro','Calendula','Geranio','Milenrama','Ortiga mayor','Pino maritimo','Quina','Sabila','Salvia','Sangre de drago','Oregano','Ispagula','Malva','Onagra','Perejil','Trigo'])
        self.declare(enfermedades_adicionales(evaluacion='y'))
        self.declare(edad(evaluacion='y'))

    #dermatologica y cicatrizantes
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion14(self):
        plantas_recomendadas.extend(['Achiote','Arnica','Col','Gualanday','Llanten','Marañon','Pam pajarito','Azucena','Cola de caballo','Higuerilla'])
        self.declare(enfermedades_adicionales(evaluacion='y')) 
        self.declare(edad(evaluacion='y'))
    
    #reproductivos y hormonales no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion15(self):
        plantas_recomendadas.extend(['Ginseng','Guarana','Anamu','Balsamina','Brusca','Calendula','Culantro','Perejil','Ruda','Sauco'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'))

    #reproductivos y hormonales embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion16(self):
        plantas_recomendadas.extend(['Sauce','Pronto alivio','Eneldo'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'))
    
    #Reglas de eliminacion
     
    #Reglas para pacientes hipertensos
    @Rule(AND(enfermedades_adicionales(enfermedades='Hipertension'),enfermedades_adicionales(evaluacion='y')))
    def eliminar_plantas1(self): 
        no_hipertensas= ['Genciana','Ginseng','Ruda']
        for planta_peligrosa in no_hipertensas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
        
    
    #Reglas para pacientes con hipoglicemia
    @Rule(AND(enfermedades_adicionales(enfermedades='Hipoglicemia'),enfermedades_adicionales(evaluacion='y')))           
    def eliminar_plantas2(self): 
        no_aptas= ['Balsamina']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
    
    #Reglas para pacientes con epilepsia
    @Rule(AND(enfermedades_adicionales(enfermedades='Epilepsia'),enfermedades_adicionales(evaluacion='y')))           
    def eliminar_plantas3(self): 
        no_aptas= ['Ajenjo']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
    
    #Reglas para pacientes con Diabetes
    @Rule(AND(enfermedades_adicionales(enfermedades='Diabetes'),enfermedades_adicionales(evaluacion='y')))           
    def eliminar_plantas4(self): 
        no_aptas= ['Algarrobo','Balsamina']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
    
    #Reglas para pacientes con Obstrupcion intestinal
    @Rule(AND(enfermedades_adicionales(enfermedades='Obstrupcion intestinal'),enfermedades_adicionales(evaluacion='y')))           
    def eliminar_plantas5(self): 
        no_aptas= ['Alcachofa','Belladona','Eucalipto','Hisopo']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
    
    
    #Reglas para niños y adolescentes menores de edad
    #Regla menores de 12
    @Rule(edad(x=P(lambda x: x >= 1) & P(lambda x: x <= 12)),edad(evaluacion='y'),salience=4)        
    def no_aptas_para_niños(self):
         print("entro 1-12")
         no_aptas= ['Albahaca','Casataña de indias','Sabila',]
         for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                 plantas_recomendadas.remove(planta_peligrosa)
    #Regla menores de 6
    @Rule(edad(x=P(lambda x: x >= 1) & P(lambda x: x <= 6)),edad(evaluacion='y'),salience=3)        
    def no_aptas_para_niños2(self):
        #print("entro 1-6:")
        no_aptas=['Cardamomo','Romero']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)

    #regla menores de 3 años 
    @Rule(edad(x=P(lambda x: x >= 1) & P(lambda x: x <= 3)),edad(evaluacion='y'),salience=2)        
    def no_aptas_para_niños3(self):
        #print("entro 1-3")
        no_aptas=['Sangre de drago']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)

    #Regla menores de 2 años
    @Rule(edad(x=P(lambda x: x >= 1) & P(lambda x: x <= 2)),edad(evaluacion='y'),salience=1)        
    def no_aptas_para_niños4(self):    
        #print("entro 1-2")
        no_aptas=['Canela','Jengibre','Pensamiento','Salvia','Verbena']
        for planta_peligrosa in no_aptas:
            if planta_peligrosa in plantas_recomendadas:
                plantas_recomendadas.remove(planta_peligrosa)
    
    #Regla Hipersensibilidades 
    @Rule(hipersensibilidad(estado='Positivo'))           
    def hipersensible(self):
        ruta_archivo = r'C:\Users\Juan José Valemcia M\Desktop\Articulos Tesisi\Sistema experto plantas\Sistema-experto-plantas-medicinales\serpm\Plantas_propiedades_arr.csv' 
        df = pd.read_csv(ruta_archivo)
        resultado= buscar_valores(df, hipsesensibilidades)
        for planta in plantas_recomendadas:
            if planta in resultado:
                plantas_recomendadas.remove(planta)
        

