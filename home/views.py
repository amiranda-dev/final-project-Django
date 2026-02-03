from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from .models import *
from .forms import *

@login_required
def index(request):
    return render(request, 'index.html')

# --- CATEGORIA ---
@login_required
def categoria(request):
    return render(request, 'categoria/lista.html', {'lista': Categoria.objects.all().order_by('-id')})

@login_required
def form_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

@login_required
def remover_categoria(request, id):
    get_object_or_404(Categoria, pk=id).delete()
    return redirect('categoria')

# --- CLIENTE ---
@login_required
def cliente(request):
    return render(request, 'cliente/lista.html', {'lista': Cliente.objects.all().order_by('-id')})

@login_required
def form_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

@login_required
def remover_cliente(request, id):
    get_object_or_404(Cliente, pk=id).delete()
    return redirect('cliente')

# --- PRODUTO ---
@login_required
def produto(request):
    return render(request, 'produto/lista.html', {'lista': Produto.objects.all()})

@login_required
def form_produto(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

@login_required
def remover_produto(request, id):
    get_object_or_404(Produto, pk=id).delete()
    return redirect('produto')

@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})

@login_required
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form = EstoqueForm(request.POST or None, instance=produto.estoque)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('produto')
    return render(request, 'produto/estoque.html', {'form': form})

# --- PEDIDO E NOTA FISCAL ---
@login_required
def pedido(request):
    return render(request, 'pedido/lista.html', {'lista': Pedido.objects.all().order_by('-id')})

@login_required
def novo_pedido(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    pedido = Pedido.objects.create(cliente=cliente)
    return redirect('detalhes_pedido', id=pedido.id)

@login_required
def detalhes_pedido(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    form = ItemPedidoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.pedido = pedido
        item.preco = item.produto.preco
        item.save()
        return redirect('detalhes_pedido', id=id)
    return render(request, 'pedido/detalhes.html', {'pedido': pedido, 'form': form})

@login_required
def editar_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, pk=id)
    form = ItemPedidoForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalhes_pedido', id=item.pedido.id)
    return render(request, 'pedido/detalhes.html', {'pedido': item.pedido, 'form': form, 'item_pedido': item})

@login_required
def remover_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    item.delete()
    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def form_pagamento(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    form = PagamentoForm(request.POST or None, instance=Pagamento(pedido=pedido))
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detalhes_pedido', id=id)
    return render(request, 'pedido/pagamento.html', {'pedido': pedido, 'form': form})

@login_required
def nota_fiscal(request, id):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente'), pk=id)
    return render(request, 'pedido/nota_fiscal.html', {'pedido': pedido})

@login_required
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
    try:
        app, modelo_name = app_modelo.split('.')
        model = apps.get_model(app, modelo_name)
        resultados = model.objects.filter(nome__icontains=termo)
        return JsonResponse([{'id': o.id, 'nome': o.nome} for o in resultados], safe=False)
    except:
        return JsonResponse([], safe=False)