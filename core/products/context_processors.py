from .models import Cart

def cart_processor(request):
    """
    Context processor to make the total number of items in the cart
    available to all templates (for the cart notification badge).
    """
    cart_item_count = 0
    if hasattr(request, 'session') and request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            # Sum up the quantities of all items in the cart
            cart_item_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            pass
            
    return {'cart_item_count': cart_item_count}
