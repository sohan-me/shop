from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product, Variation
from cart.models import Cart, CartItem
# Create your views here.!


def _cart_id(request):

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product_id, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)

            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

    if cart_item_exist:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        ex_variation_list = []
        cart_item_id = []
        
        for cart_item in cart_items:
            existing_variation = cart_item.product_variation.all()
            ex_variation_list.append(list(existing_variation))
            cart_item_id.append(cart_item.id)

        if product_variation in ex_variation_list:
            index = ex_variation_list.index(product_variation)
            cart_item_id = cart_item_id[index]
            cart_item = CartItem.objects.get(product=product, id=cart_item_id)
            cart_item.quality += 1
            cart_item.save()
        
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quality=1)
            if len(product_variation) > 0:
                cart_item.product_variation.add(*product_variation)
            else:
                pass
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quality=1)
        if len(product_variation) > 0:
            cart_item.product_variation.add(*product_variation)
        cart_item.save()

    return redirect('cart:cart')


def remove_from_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)

    try:

        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quality > 1:
            cart_item.quality -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart:cart')


def delete_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
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
