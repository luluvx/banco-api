from django.db import models
import random
from banco.models import CustomUser


class CuentaBancaria(models.Model):
    numero_cuenta = models.IntegerField( unique=True, editable=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Cuenta {self.numero_cuenta} de {self.user.first_name} {self.user.last_name}    '


    def save(self, *args, **kwargs):
        if not self.numero_cuenta:
            self.numero_cuenta = self.generar_numero_cuenta()
        super().save(*args, **kwargs)

    def generar_numero_cuenta(self):
        while True:
            numero = str(random.randint(1000000000, 9999999999))
            if not CuentaBancaria.objects.filter(numero_cuenta=numero).exists():
                return numero



