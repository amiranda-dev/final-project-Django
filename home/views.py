from django.shortcuts import render
from .models import *
from .forms import *


def index(request):
    return render(request,'index.html')


def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)


def form_categoria(resquest):
    form = CategoriaForm()
    contexto = {
        'form':form,
    }
    return render(resquest, 'categoria/formulario.html', contexto)
        