from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .simple_serializers import UserSimpleSerializer
from .movimiento_viewset import MovimientoSerializer
from banco.models import CuentaBancaria, CustomUser, Movimiento


class CuentaBancariaSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(
        read_only=True,
        many=False,
    )

    class Meta:
        model = CuentaBancaria
        fields = '__all__'
        read_only_fields = ['user']



class CuentaBancariaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CuentaBancaria.objects.all()
    serializer_class = CuentaBancariaSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action (detail=False, methods=['get'], url_path='mis-cuentas')
    def mis_cuentas(self, request):
        user = self.request.user
        cuentas = CuentaBancaria.objects.filter(user=user)
        serializer = self.get_serializer(cuentas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='movimientos')
    def movimientos(self, request, pk=None):
        user = self.request.user

        cuenta = CuentaBancaria.objects.filter(user=user, id=pk).first()

        if not cuenta:
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        movimientos = Movimiento.objects.filter(cuenta=cuenta)
        serializer = MovimientoSerializer(movimientos, many=True)

        if not serializer.data:
            return Response({'message': 'No tienes movimientos en esta cuenta'}, status=404)
        return Response(serializer.data)







