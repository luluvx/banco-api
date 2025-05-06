from rest_framework import serializers

from banco.models import CustomUser, Transferencia, CuentaBancaria


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'ci']

class CuentaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaBancaria
        fields = ['id', 'numero_cuenta', 'saldo', 'user']
