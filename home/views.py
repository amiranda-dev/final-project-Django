from django.shortcuts import get_object_or_404, render, redirect

from .models import *

from .forms import *

from django .contrib import messages

from django.http import JsonResponse

from django.apps import apps

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html',contexto)


# Formulário de Categoria
@login_required
def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)


# Editar Categoria
@login_required
def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem
     
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria') # redireciona para a listagem
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})


# View para exibir detalhes 
@login_required
def detalhes_categoria(request, id):
    categoria = Categoria.objects.get(pk=id) # Busca a categoria no banco [cite: 12]
    return render(request, 'categoria/detalhes.html', {'item': categoria}) 

# View para remover categoria 
@login_required
def remover_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    categoria.delete() # Exclui o registro
    return redirect('categoria') # Redireciona para listagem 

# View para listar clientes
@login_required
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html',contexto)

# View para o formulário de cliente
@login_required
def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('cliente')
        else:
            # Opcional: Mensagem genérica, pois os erros específicos 
            # estarão no form.errors dentro do template.
            messages.error(request, 'Erro ao salvar o registro. Verifique os campos.')
    else:
        form = ClienteForm() # Método GET: Formulário vazio
    
    contexto = {'form': form}
    return render(request, 'cliente/formulario.html', contexto)


# --- ADICIONE ISSO AO FINAL DO SEU VIEWS.PY ---

# View para Editar Cliente
@login_required
def editar_cliente(request, id):
    try:
        cliente_instancia = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente_instancia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=cliente_instancia)
    
    return render(request, 'cliente/formulario.html', {'form': form})

# View para Remover Cliente
@login_required
def remover_cliente(request, id):
    try:
        cliente_instancia = Cliente.objects.get(pk=id)
        cliente_instancia.delete()
        messages.success(request, 'Cliente removido com sucesso!')
    except Cliente.DoesNotExist:
        messages.error(request, 'Erro ao remover: Cliente não encontrado')
    
    return redirect('cliente')


# ... (mantenha o código anterior de categoria e cliente como está)

# --- VIEWS DE PRODUTO (Baseado no Slide 13 e no seu arquivo lista.html) ---

# View para listar produtos 
@login_required
def produto(request):
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

# View para o formulário de produto
@login_required
def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    else:
        form = ProdutoForm()
    
    # Verifique se o nome do arquivo é formulario.html ou form.html (seu zip veio como form.html)
    return render(request, 'produto/form.html', {'form': form})

# View para Editar Produto (Necessária para o botão Editar do lista.html)
@login_required
def editar_produto(request, id):
    item = Produto.objects.get(pk=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado!')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=item)
    return render(request, 'produto/form.html', {'form': form})

# View para Remover Produto (Necessária para o botão Remover do lista.html)
@login_required
def remover_produto(request, id):
    item = Produto.objects.get(pk=id)
    item.delete()
    messages.success(request, 'Produto removido!')
    return redirect('produto')

# View para Detalhes do Produto
@login_required
def detalhes_produto(request, id):
    item = Produto.objects.get(pk=id)
    return render(request, 'produto/detalhes.html', {'item': item})

# View para Ajustar Estoque do Produto
@login_required
def ajustar_estoque(request, id):
    produto = produto = Produto.objects.get(pk=id)
    estoque = produto.estoque # pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto) 
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form,})


# View de teste1
@login_required
def teste1(request):
    return render(request,'testes/teste1.html')
# View de teste2
@login_required
def teste2(request):
    return render(request, 'testes/teste2.html')

# View para busca genérica de dados (autocomplete)
@login_required
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

# View para exibir detalhes do cliente
@login_required
def detalhes_cliente(request, id):
    try:
        cliente_instancia = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado')
        return redirect('cliente')
        
    return render(request, 'cliente/detalhes.html', {'item': cliente_instancia})

# View para listar pedidos
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')  # Obtém todos os registros
    return render(request, 'pedido/lista.html', {'lista': lista})

# View para criar um novo pedido
@login_required
def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  # Redireciona para a listagem
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)# cria um formulario com o novo pedido
        return render(request, 'pedido/form.html',{'form': form,})
    else: # se for metodo post, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido')


# View para exibir detalhes do pedido
@login_required
def detalhes_pedido(request, id):
    pedido = get_object_or_404(Pedido, pk=id) 
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False) 
            item_pedido.preco = item_pedido.produto.preco 
            
            estoque_atual = item_pedido.produto.estoque.qtde 
            if estoque_atual >= item_pedido.qtde:
                item_pedido.produto.estoque.qtde -= item_pedido.qtde 
                item_pedido.produto.estoque.save()
                
                item_pedido.pedido = pedido
                item_pedido.save() 
                messages.success(request, 'Produto adicionado!')
                return redirect('detalhes_pedido', id=id) # Redireciona para limpar o POST
            else:
                messages.error(request, f'Estoque insuficiente: {estoque_atual}') 
    else:
        form = ItemPedidoForm()

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)
               
# View para editar item do pedido 
@login_required    
def editar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, pk=id)
    quantidade_anterior = item_pedido.qtde 
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            diferenca = item_pedido.qtde - quantidade_anterior 
            estoque = item_pedido.produto.estoque
            
            if estoque.qtde >= diferenca: 
                estoque.qtde -= diferenca 
                estoque.save()
                item_pedido.save()
                return redirect('detalhes_pedido', id=item_pedido.pedido.id) #
            else:
                messages.error(request, 'Estoque insuficiente.') 
    else:
        form = ItemPedidoForm(instance=item_pedido) 

    return render(request, 'pedido/form.html', {'form': form, 'item': item_pedido})
    
# View para remover item do pedido
@login_required
def remover_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    
    # Devolve a quantidade ao estoque antes de excluir
    estoque = item.produto.estoque
    estoque.qtde += item.qtde
    estoque.save()
    
    item.delete()
    messages.success(request, 'Item removido e estoque devolvido.')
    return redirect('detalhes_pedido', id=pedido_id)























