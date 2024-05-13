from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria, Review
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import ReviewForm
from django.db.models import Avg
from django.http import JsonResponse


def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


def inf_empresa(request):
    return render(request, 'inf.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passwd']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Olá de novo, {}!".format(user.username))
            return redirect('home')
        else:
            messages.error(request, "Credenciais inválidas, tente de novo!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Obrigado pela sua visita!")
    return redirect('home')


def produto(request, pk):
    produto_solicitado = Produto.objects.get(id=pk)
    avaliacoes = produto_solicitado.review_set.all()
    media_avaliacoes = calcular_media_avaliacoes(pk)

    return render(request, 'produto.html',
                  {'produto': produto_solicitado, 'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes})


def categoria(request, abc):
    abc = abc.replace('-', ' ')

    try:
        categoria_solicitada = Categoria.objects.get(nome=abc)
        produtos = Produto.objects.filter(categoria=categoria_solicitada)
        return render(request, 'categoria.html', {'produtos': produtos, 'categoria': categoria_solicitada})
    except:
        messages.success(request, "A categoria em questão é inexistente!")
        return redirect('home')


def registo_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Este nome de usuário já está em uso. Por favor, escolha outro.")
                return redirect('registo')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                messages.success(request, "Usuário registrado com sucesso. Por favor, faça login.")
                return redirect('login')
        else:
            messages.error(request, "As senhas não coincidem. Por favor, tente novamente.")
            return redirect('registo')
    else:
        return render(request, 'registo.html', {})


def atualizar_credenciais(request):
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')

        if new_username:
            user.username = new_username
            user.save()
            messages.success(request, "Nome de usuário atualizado com sucesso.")
            return redirect('atualizar_credenciais')

        if new_password1 and new_password2:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha atualizada com sucesso.")
                return redirect('atualizar_credenciais')
            else:
                messages.error(request, "As senhas não coincidem. Por favor, tente novamente.")
                return redirect('atualizar_credenciais')
    else:
        return render(request, 'atualizar_credenciais.html', {})


def calcular_media_avaliacoes(produto_id):
    media_avaliacoes = Review.objects.filter(item_id=produto_id).aggregate(Avg('rating'))['rating__avg']
    return media_avaliacoes if media_avaliacoes else 0


@login_required
def review_page(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    avaliacao_existente = Review.objects.filter(item=produto, user=request.user).exists()

    if avaliacao_existente:
        messages.success(request, "Ja avaliou este produto.")
        return redirect('produto', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = produto
            review.save()
            return redirect('produto', pk=pk)

    else:
        form = ReviewForm()

    return render(request, 'review_page.html', {'form': form, 'produto': produto})


def resumo_carrinho(request):
    carrinho = request.session.get('carrinho', [])
    produtos_no_carrinho = Produto.objects.filter(id__in=carrinho)

    quantidade_por_produto = {}
    for produto_id in carrinho:
        produto_id_str = str(produto_id)
        if produto_id_str in quantidade_por_produto:
            quantidade_por_produto[produto_id_str] += 1
        else:
            quantidade_por_produto[produto_id_str] = 1

    total = sum(
        (produto.preco_saldo if produto.em_saldo else produto.preco) * quantidade_por_produto[str(produto.id)] for
        produto in produtos_no_carrinho)

    produtos_com_quantidade = [(produto, quantidade_por_produto[str(produto.id)]) for produto in produtos_no_carrinho]

    return render(request, "resumo_carrinho.html", {'produtos': produtos_com_quantidade, 'total': total})


def add_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', [])
    carrinho.append(produto_id)
    request.session['carrinho'] = carrinho
    return redirect('resumo_carrinho')


def limpar_carrinho(request):
    try:
        del request.session['carrinho']
        return JsonResponse({'success': True})
    except KeyError:
        return JsonResponse({'success': False, 'error': 'O carrinho já está vazio.'})


def realizar_pagamento(request):
    if request.user.is_authenticated:
        try:
            if len(request.session.get('carrinho', [])) > 0:
                del request.session['carrinho']
                return redirect('sucesso_encomenda')
            else:
                messages.error(request, "Seu carrinho está vazio. Adicione produtos antes de realizar o pagamento.")
                return redirect('resumo_carrinho')
        except KeyError:
            pass
        return redirect('sucesso_encomenda')
    else:
        messages.error(request, "Você precisa fazer login para completar a compra.")
        return redirect('login')


def sucesso_encomenda(request):
    return render(request, 'sucesso_encomenda.html')
