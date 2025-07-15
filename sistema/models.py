from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = (
        ('cliente', 'Cliente'),
        ('funcionario', 'Funcionário'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.user.username} ({self.tipo})"

class Produto(models.Model):
    TIPO_CHOICES = [
        ('frios', 'Frios'),
        ('paes', 'Pães'),
        ('bebidas', 'Bebidas'),
        ('doces', 'Doces'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # 👈 NOVO CAMPO

    def __str__(self):
        return self.nome
