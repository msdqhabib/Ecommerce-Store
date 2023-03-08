from django.shortcuts import render
from store.models import Product

def home(request):
    #is_available only bring available products 
    products = Product.objects.all().filter(is_available=True)
    context = { 'products': products}
    return render(request, 'index.html',context)