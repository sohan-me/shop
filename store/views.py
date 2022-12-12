from multiprocessing import context
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Product, ReviewRating
from core.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewRatingForm
from django.contrib import messages
from orders.models import OrderProduct
from accounts.models import UserProfile
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

    orderproduct = None
    try:
        product_details = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        return e

    try:
        if request.user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product_details.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None

    review = ReviewRating.objects.filter(product_id=product_details.id, status=True)
    context = {'product_details': product_details, 'orderproduct':orderproduct, 'review':review}
    return render(request, 'store/product_details.html', context)


def search(request, product=None, product_count=0):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = product.count()   
          
    context = {'products': product, 'product_count': product_count}
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":

        try:
            ratings = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=ratings)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        
        except:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)