from .models import Cart, CartItem
from .views import _cart_id


def counter_itens_cart(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            user = request.user
            if request.user.is_authenticated:
                cart_itens = CartItem.objects.all().filter(user=user)
            else:
                cart_itens = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_itens:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)


