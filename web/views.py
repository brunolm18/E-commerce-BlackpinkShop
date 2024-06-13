from django.shortcuts import render,get_object_or_404,redirect
from . models import Categoria,Producto
from .carrito import Cart
# Create your views here.
"""vistas para el catalogo de productos"""

def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {
        "productos":listaProductos,
        "categorias":listaCategorias
    }
    return render(request,'index.html',context)


def productosPorCategoria(request,categoria_id):
    '''vista para filtrar productos por categoria'''
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all() # type: ignore

    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'productos': listaProductos
    }
    return render(request,'index.html',context)


def productosPorNombre(request):
    '''vista para filtrado de productos por nombre'''
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias':listaCategorias,
        'productos': listaProductos,
    }
    return render(request,'index.html',context)

def productoDetalle(request,producto_id):
    '''vista para el detalle del producto'''

    objProducto = get_object_or_404(Producto,pk=producto_id)
    context = {
        'producto':objProducto

    }
    return render(request,'producto.html',context)



"""Vistas para el carrito de compras"""

def carrito(request):
    return render(request,'carrito.html')


def agregarCarrito(request,producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST ['cantidad'])
    else:
        cantidad = 1

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto,cantidad)

    if request.method == "GET":
        return redirect('/')

    return render(request,'carrito.html')


def eliminarProductoCarrito(request,producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request,'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request,'carrito.html')