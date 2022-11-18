from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product, Variation
from cart.models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.!


def _cart_id(request):

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):

    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_variation = []

    if current_user.is_authenticated:

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

        cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()

        if cart_item_exist:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
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
                messages.success(request, 'Product Quantity Updated.')
            
            else:

                cart_item = CartItem.objects.create(product=product, user=current_user, quality=1)
                if len(product_variation) > 0:
                    cart_item.product_variation.add(*product_variation)
                else:
                    pass
                cart_item.save()
                messages.success(request, f'{product.product_name} Added to Cart.')
        else:

            cart_item = CartItem.objects.create(product=product, user=current_user, quality=1)
            if len(product_variation) > 0:
                cart_item.product_variation.add(*product_variation)
                cart_item.save()
            messages.success(request, f'{product.product_name} Added to Cart.')
            

        return redirect('cart:cart')

    else:

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
                messages.success(request, 'Product Quantity Updated.')
            
            else:
                cart_item = CartItem.objects.create(product=product, cart=cart, quality=1)
                if len(product_variation) > 0:
                    cart_item.product_variation.add(*product_variation)
                else:
                    pass
                cart_item.save()
                messages.success(request, f'{product.product_name} Added to Cart.')
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quality=1)
            if len(product_variation) > 0:
                cart_item.product_variation.add(*product_variation)
            cart_item.save()
            messages.success(request, f'{product.product_name} Added to Cart.')
            

        return redirect('cart:cart')


def remove_from_cart(request, product_id, cart_item_id):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except:
        cart = None
    product = Product.objects.get(id=product_id)


    try:
        if request.user.is_authenticated:
            cart_item =  CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quality > 1:
            cart_item.quality -= 1
            cart_item.save()
            messages.success(request, 'Product Quantity Updated.')
        else:
            cart_item.delete()
            messages.success(request, f'{product.product_name} has been removed.')
    except:
        pass

    return redirect('cart:cart')


def delete_cart_item(request, product_id, cart_item_id):

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
    cart_item.delete()
    messages.success(request, f'{product.product_name} has beem removed.')

    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None, tax=None, grand_total=None):

    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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



@login_required(login_url='accounts:log_in')
def checkout(request, total=0, quantity=0, cart_items=None, tax=None, grand_total=None):

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        
        else:
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

    return render(request, 'cart/checkout.html', context)


 