from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from banco.apis import UserSimpleSerializer
from banco.models import Beneficiario


class BeneficiarioSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(
        read_only=True,
        many=False,
    )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        read_only_fields = ['user']


class BeneficiarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Beneficiario.objects.all()
    serializer_class = BeneficiarioSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='mis-beneficiarios')
    def mis_beneficiarios(self, request):
        user = self.request.user
        beneficiarios = Beneficiario.objects.filter(user=user)
        serializer = self.get_serializer(beneficiarios, many=True)

        if not serializer.data:
            return Response({'message': 'No tienes beneficiarios registrados'}, status=404)

        return Response(serializer.data)