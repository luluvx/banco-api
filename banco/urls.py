from django.urls import path, include
from rest_framework import routers

from banco.apis import UserViewSet, BeneficiarioViewSet, CuentaBancariaViewSet, TransferenciaViewSet, AuthViewSet, \
    MovimientoViewSet

router = routers.DefaultRouter()

router.register('beneficiarios', BeneficiarioViewSet)
router.register("cuentas", CuentaBancariaViewSet)
router.register("transferencias",TransferenciaViewSet)

router.register('movimientos', MovimientoViewSet, basename='movimientos')
router.register('transferencias', TransferenciaViewSet, basename='transferencias')



router.register("usuarios", UserViewSet, basename='usuarios')
router.register("auth", AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls))
]