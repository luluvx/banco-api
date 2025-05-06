from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from banco.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'ci']


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AuthViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        username = request.data.get('username')
        password = request.data.get('password')
        ci= request.data.get('ci')

        if not nombre or not apellido or not username or not password or not ci:
            return Response({'error': 'El nombre, apellido, username, contraseña y ci son requeridos'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'El nombre de usuario ya existe'}, status=400)
        if CustomUser.objects.filter(ci=ci).exists():
            return Response({'error': 'El CI ya existe'}, status=400)


        user = CustomUser.objects.create_user(first_name=nombre, last_name=apellido, username=username, password=password, ci=ci)
        return Response({'id': user.id, 'nombre': user.first_name, 'apellido': user.last_name, 'username': user.username}, status=201)