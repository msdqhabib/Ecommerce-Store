from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import Product,Variation
from .models import Cart,CartItems
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#adding _ before mean its a private fxn
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #Get product
    #if user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
        #To make it dynamic we loop through it get the value instead of manually getting only color and size
         for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                #iexact will ignore if key is capital or in small letter
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

        
        Is_cart_item_exists = CartItems.objects.filter(product=product,user=current_user).exists()
        if Is_cart_item_exists:
            cart_item = CartItems.objects.filter(product=product,user=current_user)
            #  existing variation -> database
            # current varriation -> product_variation
            #item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                # Increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItems.objects.create(product = product,quantity = 1,user = current_user,)
                if len(product_variation) > 0:
                    item.variations.clear()
                    # * will make sure it will add all products               
                    item.variations.add(*product_variation)
                        # cart_item.quantity += 1  #cart_item.quantity = cart_item.quantity +1
                    item.save()
        else:
            cart_item = CartItems.objects.create(product = product,quantity = 1,user = current_user,)
            if len(product_variation) > 0:
                cart_item.variations.clear() 
                # * will make sure it will add all products
                cart_item.variations.add(*product_variation)             
            cart_item.save()

        return redirect(reverse('cart'))
    
    #if user is not authenticated
    else:    
        product_variation = []
        if request.method == 'POST':
        #To make it dynamic we loop through it get the value instead of manually getting only color and size
         for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                #iexact will ignore if key is capital or in small letter
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
            #    color = request.POST['color']
            #    size = request.POST['size']
            # print(key,value)
        # return HttpResponse(color +"" +size)
        
        try:
            #Get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        Is_cart_item_exists = CartItems.objects.filter(product=product,cart=cart).exists()
        if Is_cart_item_exists:
            cart_item = CartItems.objects.filter(product=product,cart=cart)
            #  existing variation -> database
            # current varriation -> product_variation
            #item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            # print(ex_var_list)
            
            if product_variation in ex_var_list:
                # Increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItems.objects.create(product = product,quantity = 1,cart = cart,)
                if len(product_variation) > 0:
                    item.variations.clear()
                    # * will make sure it will add all products               
                    item.variations.add(*product_variation)
                        # cart_item.quantity += 1  #cart_item.quantity = cart_item.quantity +1
                    item.save()
        else:
            cart_item = CartItems.objects.create(product = product,quantity = 1,cart = cart,)
            if len(product_variation) > 0:
                cart_item.variations.clear() 
                # * will make sure it will add all products
                cart_item.variations.add(*product_variation)             
            cart_item.save()

        return redirect(reverse('cart'))


def remove_cart(request,product_id,cart_item_id):      
    product = get_object_or_404(Product,id=product_id)
    try:
       if request.user.is_authenticated:
          cart_item = CartItems.objects.get(product=product,user=request.user,id=cart_item_id)
       else:
          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_item = CartItems.objects.get(product=product,cart=cart,id=cart_item_id)
       
       if cart_item.quantity > 1:
          cart_item.quantity -= 1
          cart_item.save()
       else:
          cart_item.delete()
    except:
        pass
    return redirect('cart')

           
def remove_cart_item(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItems.objects.get(product=product,cart=cart,id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           #for logged in user
           cart_items = CartItems.objects.filter(user=request.user, is_active=True)    
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItems.objects.filter(cart=cart, is_active=True) 
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        #Implementing 5% tax on every purchase
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        "total":total,
        "quantity": quantity,
        "cart_items":cart_items,
        "tax":tax,
        "grand_total":grand_total,
    }

    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
           #for logged in user
           cart_items = CartItems.objects.filter(user=request.user, is_active=True)    
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        #Implementing 5% tax on every purchase
        tax = (5 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        "total":total,
        "quantity": quantity,
        "cart_items":cart_items,
        "tax":tax,
        "grand_total":grand_total,
    }

    return render(request, 'store/checkout.html', context)