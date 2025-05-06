from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from banco.apis import CuentaSimpleSerializer
from banco.models import Movimiento, CuentaBancaria


class MovimientoSerializer(serializers.ModelSerializer):

    cuenta_id =serializers.PrimaryKeyRelatedField(
        queryset=CuentaBancaria.objects.all(),
        source='cuenta',
        write_only=True
    )
    cuenta = CuentaSimpleSerializer(
        read_only=True,
        many=False
    )

    class Meta:
        model = Movimiento
        fields = '__all__'

    def validate(self, attrs):
        if 'cuenta' not in attrs:
            raise serializers.ValidationError('La cuenta es obligatoria')
        if attrs['tipo'] == 'egreso':
            if attrs['cuenta'].saldo < attrs['monto']:
                raise serializers.ValidationError('No hay suficiente saldo')
        if attrs['monto'] <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a 0')
        return attrs

    def create(self, validated_data):
        cuenta = validated_data['cuenta']
        monto = validated_data['monto']
        tipo = validated_data['tipo']

        if tipo == 'egreso':
            cuenta.saldo -= monto
        else:
            cuenta.saldo += monto
        cuenta.save()
        return Movimiento.objects.create(**validated_data)


class MovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer










