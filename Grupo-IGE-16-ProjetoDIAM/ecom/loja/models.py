from django.db import models
import datetime
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='uploads/produto')
    em_saldo = models.BooleanField(default=False)
    preco_saldo = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.nome


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #
    item = models.ForeignKey(Produto, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"Review de {self.user.username} em {self.item.nome}"
