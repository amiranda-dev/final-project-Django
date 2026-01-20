from django import forms
from .models import *
from datetime import date # Necessário para a validação da data 


# Categoria Form
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome  
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem


# Cliente Form
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'), # [cite: 38]
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        # Validação conforme o slide 12 
        if datanasc and datanasc > date.today():
            raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return datanasc


# === ADICIONE A CLASSE PRODUTOFORM 
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64'] 
        widgets = {
            # 'categoria': forms.Select(attrs={'class': 'form-control'}), 
            'categoria': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}), 
            'img_base64': forms.HiddenInput(), 
            'preco': forms.TextInput(attrs={
                'class': 'money form-control', 
                'maxlength': '500', 
                'placeholder': '0.000,00'
            }), 
        }

    # Função __init__ para localização do preço 
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True 
        self.fields['preco'].widget.is_localized = True

#Estoque Form
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto','qtde']
        
        widgets = {
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID do produto
            'qtde':forms.TextInput(attrs={'class': 'inteiro form-control',}),
    }
      
# Pedido Form  
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto para armazenar o ID
        }


# ItemPedido Form
class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido','produto', 'qtde']


        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'qtde':forms.TextInput(attrs={'class': 'form-control',}),
        }

    