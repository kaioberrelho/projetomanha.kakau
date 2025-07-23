from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, UserViewSet, login_view
from .views import reset_password_request, reset_password_confirm

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),
    path('reset-password/', reset_password_request, name='reset_password_request'),  # POST: recebe email
    path('reset-password-confirm/<str:uidb64>/<str:token>/', reset_password_confirm, name='reset_password_confirm'),  # POST: recebe nova senha
]