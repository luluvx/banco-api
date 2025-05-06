from django.db import models

from banco.models import CuentaBancaria


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=21, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.tipo} de {self.monto} en {self.fecha}'
