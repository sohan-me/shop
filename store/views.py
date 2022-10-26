from multiprocessing import context
from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Product
from core.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here!.


def store(request, category_slug=None):
    categories = None
    product = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.filter(category=categories, is_available=True)
        product_count = product.count()
        paginator = Paginator(product, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        product = Product.objects.filter(is_available=True)
        product_count = product.count()
        paginator = Paginator(product, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {'products': paged_products, 'product_count': product_count, }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):

    try:
        product_details = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        return e
    context = {'product_details': product_details}
    return render(request, 'store/product_details.html', context)


def search(request, product=None, product_count=0):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = product.count()   
          
    context = {'products': product, 'product_count': product_count}
    return render(request, 'store/store.html', context)
