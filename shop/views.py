from django.shortcuts import render, HttpResponse
from store.models import Product, ReviewRating
# Create your views here.


def home(request):
    product = Product.objects.filter(is_available=True).order_by('created_date')
    context = {'products': product}
    return render(request, 'home.html', context)
