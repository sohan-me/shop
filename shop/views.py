from django.shortcuts import render, HttpResponse
from store.models import Product
# Create your views here.


def home(request):
    product = Product.objects.all().filter(is_available=True)
    context = {'products': product}
    return render(request, 'home.html', context)
