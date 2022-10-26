from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from cart.models import Cart, CartItem
# Create your views here.!


def _cart_id(request):

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)  # get the product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quality += 1  # For increment of quantity (By 1)
        cart_item.save()
    except:
        cart_item = CartItem.objects.create(
            product=product,
            quality=1,
            cart=cart
        )
    cart_item.save()

    return redirect('cart:cart')


def remove_from_cart(request, product_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quality > 1:
        cart_item.quality -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart')


def delete_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart')


def cart(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = None
    grand_total = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quality)
            quantity = cart_item.quality

        tax = (total / 100) * 2
        grand_total = total + tax

    except:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'cart/cart.html', context)
