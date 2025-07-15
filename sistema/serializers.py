from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto, Perfil

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tipo = serializers.ChoiceField(choices=Perfil.TIPOS, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tipo']  # tipo está aqui apenas para input, não para output

    def create(self, validated_data):
        tipo = validated_data.pop('tipo')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Perfil.objects.create(user=user, tipo=tipo)
        return user
