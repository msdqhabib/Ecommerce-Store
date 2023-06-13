from carts.models import Cart,CartItems
from carts.views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            #This _cart_id contain session key
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
               cart_items = CartItems.objects.all().filter(user=request.user)
            else:
               cart_items = CartItems.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                print(cart_item.quantity)
                cart_count += cart_item.quantity 
                # cart_count += 1
        except Cart.DoesNotExist:
            cart_count = 0
        return dict(cart_count = cart_count)
