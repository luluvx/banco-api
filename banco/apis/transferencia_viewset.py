from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from banco.apis import BeneficiarioSerializer
from banco.apis.simple_serializers import CuentaSimpleSerializer
from banco.models import Transferencia, CuentaBancaria, Beneficiario, Movimiento


class TransferenciaSerializer(serializers.ModelSerializer):
    cuenta_origen_id = serializers.PrimaryKeyRelatedField(
        queryset=CuentaBancaria.objects.all(),
        source='cuenta_origen',
        write_only=True,
    )
    beneficiario_id = serializers.PrimaryKeyRelatedField(
        queryset=Beneficiario.objects.all(),
        source='beneficiario',
        write_only=True,
    )
    beneficiario = BeneficiarioSerializer(
        read_only=True,
    )
    cuenta_origen = CuentaSimpleSerializer(
        read_only=True,
        many=False,
    )

    class Meta:
        model = Transferencia
        fields = '__all__'



class TransferenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transferencia.objects.all()
    serializer_class = TransferenciaSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cuenta_origen = serializer.validated_data['cuenta_origen']
        beneficiario = serializer.validated_data['beneficiario']
        monto = serializer.validated_data['monto']

        if cuenta_origen.saldo < monto:
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
        if cuenta_origen.numero_cuenta == beneficiario.numero_cuenta:
            return Response({'error': 'No se puede transferir a la misma cuenta'}, status=status.HTTP_400_BAD_REQUEST)


        numero_cuenta_beneficiario = CuentaBancaria.objects.filter(numero_cuenta=beneficiario.numero_cuenta).first()
        if not numero_cuenta_beneficiario:
            return Response({'error': 'No existe la cuenta del beneficiario'}, status=status.HTTP_400_BAD_REQUEST)

        cuenta_origen.saldo -= monto
        cuenta_origen.save()
        numero_cuenta_beneficiario.saldo += monto
        numero_cuenta_beneficiario.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        Movimiento.objects.create(
            cuenta=cuenta_origen,
            tipo='egreso',
            monto=monto,
        )
        Movimiento.objects.create(
            cuenta=numero_cuenta_beneficiario,
            tipo='ingreso',
            monto=monto,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)