from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('informações/', views.inf_empresa, name='inf_empresa'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('produto/<int:pk>/', views.produto, name='produto'),
    path('categoria/<str:abc>/', views.categoria, name='categoria'),
    path('registo/', views.registo_usuario, name='registo'),
    path('atualizar_credenciais/', views.atualizar_credenciais, name='atualizar_credenciais'),
    path('avaliacao/<int:pk>/', views.review_page, name='review_page'),
    path('resumo_carrinho/', views.resumo_carrinho, name="resumo_carrinho"),
    path('add/<int:produto_id>/', views.add_carrinho, name="add_carrinho"),
    path('clear_cart/', views.limpar_carrinho, name='limpar_carrinho'),
    path('realizar_pagamento/', views.realizar_pagamento, name='realizar_pagamento'),
    path('sucesso_encomenda/', views.sucesso_encomenda, name='sucesso_encomenda'),

]
