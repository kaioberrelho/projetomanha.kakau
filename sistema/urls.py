from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, UserViewSet, login_view

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),  # 👈 Essa é a nova rota
]