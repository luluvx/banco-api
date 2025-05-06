from django.db import models

from banco.models import CustomUser


class Beneficiario(models.Model):
    nombre = models.CharField(max_length=20)
    numero_cuenta = models.IntegerField(unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='beneficiarios', null=True, blank=True)

    def __str__(self):
        return self.nombre