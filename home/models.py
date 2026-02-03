import locale
from django.db import models
from decimal import Decimal


ALIQUOTA_ICMS = 18.0
ALIQUOTA_IPI = 4.0
ALIQUOTA_PIS = 1.65
ALIQUOTA_COFINS = 7.6
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome
    

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15,verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")


    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None
    

# home/produtos.py
class Produto(models.Model):
    nome = models.CharField(max_length=100) 
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False) 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True) 

    def __str__(self):
        return self.nome 
    
    @property
    def estoque(self):
        # Tenta buscar o estoque, se não existir, cria um novo com qtde 0
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        print(flag_created)
        return estoque_item

    
# home/Estoque.py
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()


    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
    
# home/Pedido.py
class Pedido(models.Model):
    

    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4


    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)
    
    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None    



    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"
        
        
        
    @property
    def total(self):
        total_pedido = sum(item.total for item in self.itempedido_set.all())
        return total_pedido

    @property
    def qtdeItens(self):
        return self.itempedido_set.count()

    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)

    @property
    def total_pago(self):
        total = sum(pagamento.valor for pagamento in self.pagamentos.all())
        return total

    @property
    def debito(self):
        return self.total - self.total_pago
    
    @property
    def icms(self):
        return self.total * (Decimal(ALIQUOTA_ICMS) / 100)

    @property
    def ipi(self):
        return self.total * (Decimal(ALIQUOTA_IPI) / 100)

    @property
    def pis(self):
        return self.total * (Decimal(ALIQUOTA_PIS) / 100)

    @property
    def cofins(self):
        return self.total * (Decimal(ALIQUOTA_COFINS) / 100)

    @property
    def total_impostos(self):
        """Soma de todos os impostos calculados"""
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def valor_final(self):
        """Total do Pedido + Soma dos Impostos"""
        return self.total + self.total_impostos
        
    @property
    def chave_acesso(self):
        """
        Gera uma chave de acesso fictícia baseada no ID, data e um número aleatório.
        Exemplo: 202601ID0001RAND9999
        """
        import random
        data_str = self.data_pedido.strftime('%Y%m%d')
        numero_aleatorio = random.randint(1000, 9999)
        return f"{data_str}{self.id:04d}{numero_aleatorio}99990001"
        


# home/ItemPedido.py
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"  
    @property
    def total(self):
        return self.qtde * self.preco
    

# home/Pagamento.py
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4


    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
    
