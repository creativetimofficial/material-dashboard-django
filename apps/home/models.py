# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Empleado
class Empleado(models.Model):
    DNIEmpleado = models.CharField(max_length=9, primary_key=True)
    nombreEmpleado = models.CharField(max_length=20)
    apellidosEmpleado = models.CharField(max_length=40)
    cargo = models.CharField(max_length=20)
    telefonoEmpleado = models.CharField(max_length=20)
    emailEmpleado = models.CharField(max_length=40)
    direccionEmpleado = models.CharField(max_length=40)
    fecha_nacEmpleado = models.DateField()
    motivo_bajaEmpleado = models.CharField(max_length=20, null=True, blank=True)
    fecha_bajaEmpleado = models.DateField(null=True, blank=True)
    contrasena = models.CharField(max_length=4)

    def _str_(self):
        return f'{self.nombreEmpleado} {self.apellidosEmpleado}'


# Socio
class Socio(models.Model):
    DNISocio = models.CharField(max_length=9, primary_key=True)
    nombreSocio = models.CharField(max_length=24)
    apellidosSocio = models.CharField(max_length=24)
    emailSocio = models.CharField(max_length=40)
    telefonoSocio = models.CharField(max_length=9)
    direccionSocio = models.CharField(max_length=40)
    fecha_nacSocio = models.DateField()
    motivo_bajaSocio = models.CharField(max_length=60, null=True, blank=True)
    fecha_bajaSocio = models.DateField(null=True, blank=True)

    def _str_(self):
        return f'{self.nombreSocio} {self.apellidosSocio}'


# Producto
class Producto(models.Model):
    ID_producto = models.CharField(max_length=13, primary_key=True)
    nombre_producto = models.CharField(max_length=24)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tallas = models.CharField(max_length=60)
    proveedor = models.CharField(max_length=24)

    def _str_(self):
        return self.nombre_producto


# Ingreso
class Ingreso(models.Model):
    id_ingreso = models.AutoField(primary_key=True)
    monto_ingreso = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f'Ingreso {self.id_ingreso}'


# Gasto
class Gasto(models.Model):
    id_gasto = models.AutoField(primary_key=True)
    monto_gasto = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f'Gasto {self.id_gasto}'


# Campana
class Campana(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada')
    ]

    id_campana = models.AutoField(max_length=10, primary_key=True)
    nombre_campana = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):  
        return f'Campana {self.id_campana}'

# Genera
class Genera(models.Model):
    id_campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    id_gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_campana', 'id_gasto')


# Ordena
class Ordena(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    fecha_gasto = models.DateField()
    hora_gasto = models.DateTimeField()

    class Meta:
        unique_together = ('id_producto', 'id_gasto')


# Compra
class Compra(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    dnisocio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fecha_compra = models.DateField()

    class Meta:
        unique_together = ('id_producto', 'dnisocio')

