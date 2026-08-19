from django.db import models

SEXO_OPCIONES =[("H","Hombre"),("M","Mujer"),("O","Otro")]
ESPECIALIDADES = [('Traumatología','Traumatología'),('Cirugía','Cirugía'),('Cardiología','Cardiología'),('Neurología','Neurología'),('Urología','Urología'),('Oftalmología','Oftalmología')]

class Paciente( models.Model ):
    nombre = models.CharField( max_length=50, null=False) 
    apellidos = models.CharField( max_length=50, null=False) 
    numID = models.CharField( max_length=20, primary_key=True, null=False, unique=True)   
    sexo = models.CharField( choices=SEXO_OPCIONES, max_length=10, null=False)            
                                                                    
class Ingreso(models.Model):
    id = models.CharField(primary_key=True, max_length=20, null=False, unique=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=None)
    edad = models.IntegerField(null=False)
    fechaIngreso = models.DateField(null=False)
    fechaAlta = models.DateField(null=True, blank=True)
    descripcion = models.CharField( max_length=2000, blank=True, null=True)
    
class Medico( models.Model ):
    numColegiado = models.CharField( max_length=100, primary_key=True,null=False)
    especialidad = models.CharField( max_length=30, choices=ESPECIALIDADES,null=False)
    ingresos = models.ManyToManyField(Ingreso)
