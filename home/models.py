from django.db import models

# Create your models here.

# Create your models here.
class Estudiantes(models.Model):
    identificacion = models.PositiveBigIntegerField()
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    genero = models.CharField(max_length=20)
    fecha_nacimiento = models.CharField(max_length=20)
    correo_electronico = models.CharField(max_length=100)
    telefono = models.CharField(max_length=200)
    comuna = models.CharField(max_length=200)
    barrio = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    estrato = models.CharField(max_length=200)
    dir_latitude = models.CharField(max_length=200)
    dir_longitude = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200)
    facultad = models.CharField(max_length=200)
    creditos_aprobados = models.PositiveBigIntegerField()
    promedio_acumulado = models.FloatField()
 ###promedio_acumulado
