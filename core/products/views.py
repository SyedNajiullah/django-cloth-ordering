from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Product, Brand, Category, Cart, CartItem

def home(request):
    products = Product.objects.all()[:8]
    return render(request, 'index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def brand_products(request, brand_name):
    brands = Brand.objects.filter(name__iexact=brand_name)
    if not brands.exists():
        from django.http import Http404
        raise Http404("No Brand matches the given query.")
    products = Product.objects.filter(brand__in=brands)
    return render(request, 'products/product_list.html', {'products': products, 'title': brands.first().name})

def category_products(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    
    # Get the category itself and all its subcategories (recursively)
    def get_all_subcategories(cat):
        subcats = list(Category.objects.filter(parent=cat))
        all_cats = [cat]
        for subcat in subcats:
            all_cats.extend(get_all_subcategories(subcat))
        return all_cats

    all_categories = get_all_subcategories(category)
    products = Product.objects.filter(category__in=all_categories)
    return render(request, 'products/product_list.html', {'products': products, 'title': category.name})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def refund(request):
    return render(request, 'refund.html')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'title': 'ALL PRODUCTS'})

def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            size = data.get('size', 'M')
            try:
                quantity = int(data.get('quantity', 1))
            except ValueError:
                quantity = 1
        except json.JSONDecodeError:
            size = 'M'
            quantity = 1
            
        product = get_object_or_404(Product, pk=pk)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        # Look for existing item with SAME size
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            size=size
        )
        
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            if quantity > 1:
                cart_item.quantity = quantity
                cart_item.save()
            
        # Recalculate total items
        total_items = sum(item.quantity for item in cart.items.all())
        return JsonResponse({'success': True, 'cart_item_count': total_items})
        
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def remove_from_cart(request, item_id):
    session_key = request.session.session_key
    if session_key:
        try:
            cart = Cart.objects.get(session_key=session_key)
            CartItem.objects.filter(id=item_id, cart=cart).delete()
        except Cart.DoesNotExist:
            pass
    return redirect('cart_view')

def checkout(request):
    session_key = request.session.session_key
    if session_key:
        try:
            cart = Cart.objects.get(session_key=session_key)
            from .models import ProductSize
            for item in cart.items.all():
                try:
                    product_size = ProductSize.objects.get(product=item.product, size=item.size)
                    if product_size.stock >= item.quantity:
                        product_size.stock -= item.quantity
                    else:
                        product_size.stock = 0 # Prevent negative stock
                    product_size.save()
                except ProductSize.DoesNotExist:
                    pass # Size was somehow removed from database, safe to ignore for mock checkout
            # Now delete the cart and content
            cart.delete()
        except Cart.DoesNotExist:
            pass
    return redirect('cart_view')
