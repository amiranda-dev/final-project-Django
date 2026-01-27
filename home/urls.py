from django.urls import path
from . import views

urlpatterns = [
    # URLs de Categoria
    path('', views.index, name="index"), 
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form', views.form_categoria, name="form_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name="detalhes_categoria"),
    path('categoria/remover/<int:id>/', views.remover_categoria, name="remover_categoria"),
    
    # URLs de Cliente
    path('cliente/', views.cliente, name="cliente"),
    path('cliente/form', views.form_cliente, name="form_cliente"),
    path('cliente/editar/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/remover/<int:id>/', views.remover_cliente, name="remover_cliente"),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name="detalhes_cliente"),

    # URLs de Produto
    path('produto/', views.produto, name='produto'),
    path('produto/form/', views.form_produto, name='form_produto'),
    path('produto/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('produto/remover/<int:id>/', views.remover_produto, name='remover_produto'),
    path('produto/ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),

    # urls de Teste
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'), # Adicione esta linha
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),

    # URLs de Pedido
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/form/<int:id>', views.novo_pedido, name='novo_pedido'),
    path('pedido/detalhes/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),
    # Verifique se os nomes coincidem com o que você usou no redirect das views
    path('pedido/item/<int:id>/editar/', views.editar_item_pedido, name='editar_item_pedido'), 
    path('pedido/item/<int:id>/remover/', views.remover_item_pedido, name='remover_item_pedido'),
]
    

