from django.shortcuts import render, get_object_or_404
from .models import Product,ProductGallery
from category.models import Category
from carts.models import CartItems
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.db.models import Q


def store(request,category_slug=None):
    categories = None
    products = None
# So if there is slug in url than it will return product onn that specific category
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
        #count() method used to count all iems
        product_count = products.count()
#Incase of no slug in url. Mean no category name in url. It will return all products
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
        product_count = Product.objects.all().count()
    
    context = {
        'products':paged_products,
        'product_count'   :product_count}
    return render(request, 'store/store.html',context)


def product_detail(request,category_slug,product_slug):
  try:
      single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
      in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
 
  except Exception as e: 
      raise e
  
  #Get the product gallery
  product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
  context = {
      'single_product': single_product,
      'in_cart': in_cart,
      'product_gallery':product_gallery
  }

  return render(request, 'store/product_detail.html',context)


#Search
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword: #if keyword means it's not blank keyword have something
            #description__icontains means it will look for whole description and if it found any thing
            #related to that keyword than it will bring that specific product
            #to look for desc and title using keywoard we cannot use directly OR operator
            # , connsidered as AND operator
            #so acheive this we use query Q
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) |  Q(product_name__icontains=keyword))
            product_count = products.count()    
            context = {
                "products":products,
                "product_count":product_count,
            }
    return render(request,'store/store.html',context)