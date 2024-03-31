from django.db import models

# Create your models here.
class Afeciones(models.Model):
    afeccion=models.CharField(verbose_name='Afeción',max_length=80,blank=False,null=False,help_text='Afección o enfermedad')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.afeccion 
    class Meta:
        verbose_name='Afección enfermedad'
        verbose_name_plural='Afecciones o Enfermedades'
        db_table='plantas_afecciones' 
        ordering=['afeccion']  

# Create your models here.
class Generos(models.Model):
    genero=models.CharField(verbose_name='Genero',max_length=20,blank=False,null=False,help_text='Genero')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.genero 
    class Meta:
        verbose_name='Genero'
        verbose_name_plural='Genenros'
        db_table='plantas_generos' 
        ordering=['genero']         

'''
class PantasMedicianles(models.Model):
    planta=models.CharField(verbose_name='Genero',max_length=20,blank=False,null=False,help_text='Genero')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.planta 
    class Meta:
        verbose_name='Pantas'
        verbose_name_plural='Plantas'
        db_table='plantas_plantas_medicinales' 
        ordering=['planta']          

        '''