from experta import *
import pandas as pd
import unittest

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

plantas_recomendadas= []
lista_busqueda =['triterpenos']

def buscar_valores(dataframe, lista_busqueda):
    resultados = []
    for valor in lista_busqueda:
        # Buscar si el valor está en cualquier parte de la columna 7
        mask = dataframe.iloc[:, 6].str.contains(valor, case=False, na=False)
        # Filtrar el DataFrame usando la máscara de la planta
        resultados.extend(dataframe.loc[mask, 'Planta '].tolist())
        #Elimino duplicados
        sin_duplicados = set(resultados)

    lista_plantas_formateadas = []
    for planta in sin_duplicados:
        # Convertimos la primera letra a mayúscula
        primera_letra = planta[0].upper()
        # Convertimos el resto de la palabra a minúscula
        resto_palabra = planta[1:].lower()
        # Combinamos la primera letra y el resto de la palabra
        planta_formateada = primera_letra + resto_palabra
        # Añadimos la palabra formateada a la lista
        lista_plantas_formateadas.append(planta_formateada)

    return lista_plantas_formateadas

class Base_de_conocimiento(KnowledgeEngine):
    
#Reglas principales primer nivel
    #Tratamiento golpes o heridas
    @Rule(SistemaAfectado(afectacion='Golpes o heridas'))
    def IdentificarAfectacion(self):
        self.declare(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'))
    #Tratamiento problemas cardiovasculares
    @Rule(SistemaAfectado(afectacion='Problemas cardiovasculares'))
    def IdentificarAfectacion2(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'))
    #Tratamiento problemas respiratorios
    @Rule(SistemaAfectado(afectacion='Problemas respiratorios'))
    def IdentificarAfectacion3(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades respiratorias'))
    #Tratamiento problemas Digestivos
    @Rule(SistemaAfectado(afectacion='Problemas digestivos'))
    def IdentificarAfectacion4(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades digestivas'))
    #Tratamiento problemas inmunologicos
    @Rule(SistemaAfectado(afectacion='Problemas inmunologicos'))
    def IdentificarAfectacion5(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'))  
    #Tratamiento problemas gastrointestinales
    @Rule(SistemaAfectado(afectacion='Problemas gastrointestinales'))
    def IdentificarAfectacion6(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'))
    #Tratamiento problemas Dermatologicos o cicatrizantes
    @Rule(SistemaAfectado(afectacion='Problemas dermatologicos o cicatrizantes'))
    def IdentificarAfectacion7(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'))
    #Tratamiento problemas reproductivos y hormonales
    @Rule(SistemaAfectado(afectacion='Problemas reproductivos y hormonales'))
    def IdentificarAfectacion8(self):
        self.declare(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'))        
        
#Reglas segundo nivel
    #AA para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion(self): 
        plantas_recomendadas.extend(['Ortiga','Verbena','Guarana','Sangre de drago','Balsamina','Culantro','Canela','Cidron','Limoncillo','Menta','Pasiflora','Mielenrama'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #AA para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Antiinflamatorios y analgesicas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion2(self):
        plantas_recomendadas.extend(['Achiote','Guaba','Aji','Arnica','Canelo de monte','Pronto alivio','Sauce','Guaba','Trigo sarraceno'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))

     #Cardiovasculares para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion3(self): 
        plantas_recomendadas.extend(['Guarana','Ortiga','Vid','Ginseng'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
     #Cardiovasculares para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades cardiovasculares'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion4(self):
        plantas_recomendadas.extend(['Cafe','Ginkgo biloba','Yarumo','Ajo','Trigo sarraceno'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    
    #Respiratorias para no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades respiratorias'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion5(self):
        plantas_recomendadas.extend(['Eucalipto','Ginseng','Hiedra','Hisopo','Jengibre','Malva','Oregano','Pensamiento','Sabila','Sauco','Verbena officinalis','Vira-vira','Cimifuga','Ruda','Violeta','Mielenrama','Guarana','Canela','Quina','Salvia'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #Respiratorias para embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades respiratorias'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion6(self):
        plantas_recomendadas.extend(['Marrubio blanco','Pronto alivio','Algarrobo','Arnica'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
        
    #Digestivas no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades digestivas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion7(self):
        plantas_recomendadas.extend(['Ajenjo','Cardamomo','Genciana','Mielenrama','Romero','Canela','Cimicifuga','Culantro','Gienseng','Oregano','Salvia'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #Digestivas embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades digestivas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion8(self):
        plantas_recomendadas.extend(['Rabano','Marrubio','Sauce','Pronto alivio','Toronjil','Valeriana','Zanahoria'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
        
    #Inunologicas no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion9(self):  
        plantas_recomendadas.extend(['Geranio','Onagra','Verbena littoralis','Balsamina','Ruda','Salvia','Ajenjo','Anamu','Eucalipto'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'))
    #Inunologicas embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades inmunologicas'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion10(self):
        plantas_recomendadas.extend(['Ginkgo biloba','Trigo sarraceno','Equinacea','Ajo','Casco de vaca','Zanahoria','Rabano'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    
    #gastrointestinales no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion11(self):   
        plantas_recomendadas.extend(['Boldo','Cascara sagrada','Ispagula','Malva','Manzanilla','Psyllium','Ruibardo','Sabila','Sauco','Sen','Balsamina','Cimicifuga','Quina','Albahaca','Limoncillo','Menta','Oregano','Perejil','Salvia','Yerbabuena'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #gastrointestinales embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades gastrointestinales'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion12(self):
        plantas_recomendadas.extend(['Higuerilla','Linaza','Papaya','Casco de vaca','Chilca','Nogal blanco','Anis','Cidron','Eneldo'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
       
    #dermatologica y cicatrizantes no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion13(self):
        plantas_recomendadas.extend(['Anamu','Balsamina','Boton negro','Calendula','Geranio','Milenrama','Ortiga mayor','Pino maritimo','Quina','Sabila','Salvia','Sangre de drago','Oregano','Ispagula','Malva','Onagra','Perejil','Trigo'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #dermatologica y cicatrizantes
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades dermatologicos o cicatrizantes'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion14(self):
        plantas_recomendadas.extend(['Achiote','Arnica','Col','Gualanday','Llanten','Marañon','Pam pajarito','Azucena','Cola de caballo','Higuerilla'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    
    #reproductivos y hormonales no embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'),AND(embarazo(estado='Negativo'),lactancia(estado= 'Negativo'))))
    def recomendacion15(self):
        plantas_recomendadas.extend(['Ginseng','Guarana','Anamu','Balsamina','Brusca','Calendula','Culantro','Perejil','Ruda','Sauco'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    #reproductivos y hormonales embarazadas
    @Rule(AND(SistemaAfectado(tratamiento= 'Propiedades reproductivos y hormonales'),OR(embarazo(estado='Positivo'),lactancia(estado="Positivo"))))
    def recomendacion16(self):
        plantas_recomendadas.extend(['Sauce','Pronto alivio','Eneldo'])
        self.declare(enfermedades_adicionales(evaluacion='y'),edad(evaluacion='y'),hipersensibilidad(estado='Positivo'))
    
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
    
    #Reglas para niños y adolescentes menores de edad
    #Regla menores de 12
    @Rule(edad(x=P(lambda x: x >= 1) & P(lambda x: x <= 12)),edad(evaluacion='y'),salience=4)        
    def no_aptas_para_niños(self):
         #print("entro 1-12")
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
        resultado= buscar_valores(df, lista_busqueda)
        for planta in plantas_recomendadas:
            if planta in resultado:
                plantas_recomendadas.remove(planta)




engine =Base_de_conocimiento()
engine.reset()
engine.declare(SistemaAfectado(afectacion='Golpes o heridas'),embarazo(estado='Positivo'),lactancia(estado='Negativo'),edad(x= 35))
engine.run()

class TestRules(unittest.TestCase):
    def test_recomendacion(self):
        engine = Base_de_conocimiento()
        engine.reset()
        engine.declare(SistemaAfectado(afectacion='Problemas respiratorios'),embarazo(estado='Negativo'),lactancia(estado='Negativo'),enfermedades_adicionales(enfermedades= 'Hipertension'),edad(x= 20))
        engine.run()
        # Verificar que la lista de plantas recomendadas sea la esperada
        expected_plants = ['Eucalipto', 'Hiedra', 'Hisopo', 'Jengibre', 'Malva', 'Oregano', 'Sabila', 'Verbena officinalis', 'Cimifuga', 'Violeta', 'Mielenrama', 'Guarana', 'Canela', 'Quina', 'Salvia']
        self.assertEqual(plantas_recomendadas, expected_plants)

#if __name__ == '__main__':
#    unittest.main()


print("Plantas: ",plantas_recomendadas)