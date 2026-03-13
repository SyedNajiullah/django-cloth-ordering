from django.shortcuts import render, get_object_or_404, redirect
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
    product = get_object_or_404(Product, pk=pk)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_view')

def checkout(request):
    session_key = request.session.session_key
    if session_key:
        Cart.objects.filter(session_key=session_key).delete()
    return redirect('cart_view')
