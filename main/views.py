from django.shortcuts import render, redirect
from .models import Product, Cart, Order
from django.http import HttpResponseBadRequest
from .models import Product, Cart

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.products.set([item.product for item in cart_items])
    cart_items.delete()
    return render(request, 'checkout.html', {'order': order})


def update_cart(request):
    if request.method == 'POST':
        for item in request.POST:
            if item.startswith('quantity_'):
                cart_item_id = item.split('_')[1]
                quantity = request.POST[item]
                if quantity.isdigit() and int(quantity) >= 1:
                    cart_item = Cart.objects.get(id=cart_item_id)
                    cart_item.quantity = int(quantity)
                    cart_item.save()
                else:
                    return HttpResponseBadRequest('Invalid quantity value.')
        return redirect('cart')
    else:
        return HttpResponseBadRequest('Only POST requests are allowed.')


