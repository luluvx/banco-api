from django.db import models

from banco.models import CuentaBancaria, Beneficiario


class Transferencia(models.Model):
    cuenta_origen = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='transferencias_origen')
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, related_name='transferencias_beneficiario')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transferencia de {self.cuenta_origen} a {self.beneficiario} por {self.monto}'