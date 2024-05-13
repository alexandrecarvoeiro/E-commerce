from django.contrib import admin
from .models import Categoria, Produto, Review

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Review)
