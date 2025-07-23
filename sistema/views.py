from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Produto, Perfil
from .serializers import ProdutoSerializer, UserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        perfil = Perfil.objects.get(user=user)
        return Response({
            'message': 'Login realizado com sucesso',
            'user_id': user.id,
            'tipo': perfil.tipo
        })
    else:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reset_password_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Usuário com esse email não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Gerar token e UID para o link
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Montar URL (exemplo, ajuste o frontend para essa URL)
    reset_link = f"http://127.0.0.1:5500/reset_senha_confirm.html?uid={uid}&token={token}"

    # Enviar email (modifique para seu template real)
    send_mail(
        subject="Redefinição de senha",
        message=f"Clique no link para redefinir sua senha: {reset_link}",
        from_email='no-reply@seudominio.com',
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({'message': 'Email de redefinição enviado.'})


@api_view(['POST'])
def reset_password_confirm(request, uidb64, token):
    password = request.data.get('password')
    if not password:
        return Response({'error': 'Senha é obrigatória'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'error': 'Link inválido'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Token inválido ou expirado'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    return Response({'message': 'Senha redefinida com sucesso.'})