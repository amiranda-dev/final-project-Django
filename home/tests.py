# O módulo os fornece funções para interagir com o sistema operacional.
import os
import sys
# O módulo django é a biblioteca principal do Django, permite acessar suas funcionalidades.
import django
sys.path.append('E:/Dropbox/Projetos/workspacePython/workTeste/cadweb')
# Essa linha define a variável de ambiente DJANGO_SETTINGS_MODULE, que informa ao Django qual arquivo de configurações (normalmente settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pweb.settings')
#Este comando inicializa o ambiente do Django. 
django.setup()

from home.models import Categoria


# Criação de uma instância de categoria e inserção no banco de dados
""""
categoria1 = Categoria(nome='Eletrodomésticos', ordem=1)
categoria1.save()

categoria1 = Categoria(nome='Eletrônicos', ordem=2)
categoria1.save()

categoria1 = Categoria(nome='Esporte e Lazer', ordem=4)
categoria1.save()

categoria1 = Categoria(nome='Ferramentas', ordem=5)
categoria1.save()

categoria1 = Categoria(nome='Moda e Acessórios', ordem=3)
categoria1.save()

"""
lista = Categoria.objects.all()
print(lista)
for categoria in lista:
    print(categoria.id, categoria.nome, categoria.ordem)

lista = Categoria.objects.filter(nome="Eletrônicos")

class Produto:
    None

produtos = Produto.objects.filter(categoria="Eletrônicos", preco__lt=1000)


print('Categoria inserida com sucesso!')
