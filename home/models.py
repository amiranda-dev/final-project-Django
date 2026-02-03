from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")

    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'

class Pedido(models.Model):
    NOVO, EM_ANDAMENTO, CONCLUIDO, CANCELADO = 1, 2, 3, 4
    STATUS_CHOICES = [(NOVO, 'Novo'), (EM_ANDAMENTO, 'Em Andamento'), (CONCLUIDO, 'Concluído'), (CANCELADO, 'Cancelado')]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"

    @property
    def total(self):
        return sum(item.qtde * item.preco for item in self.itempedido_set.all())
    
    @property
    def total_pago(self):
        return sum(pagamento.valor for pagamento in Pagamento.objects.filter(pedido=self))    
    
    @property
    def debito(self):
        return self.total - self.total_pago

    # Propriedades para a Nota Fiscal
    @property
    def chave_acesso(self):
        if self.id and self.data_pedido:
            return f"3124{self.data_pedido.strftime('%Y%m%d')}{self.id:010d}000100000000123456789"
        return "AGUARDANDO"

    @property
    def imposto(self):
        return float(self.total) * 0.10

    @property
    def total_com_imposto(self):
        return float(self.total) + self.imposto

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.preco * self.qtde

class Pagamento(models.Model):
    FORMA_CHOICES = [(1, 'Dinheiro'), (2, 'Cartão'), (3, 'Pix'), (4, 'Outra')]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pgto = models.DateTimeField(auto_now_add=True)