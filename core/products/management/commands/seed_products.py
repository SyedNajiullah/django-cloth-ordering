from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product, ProductSize, ProductImage
from django.core.files import File
import os
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with dummy products, brands, and categories'

    def handle(self, *args, **kwargs):
        # Create Brands
        brands_list = ["barba napoli", "Brunello Cucinelli", "Isaia", "premiata"]
        brands = {}
        for name in brands_list:
            brand, created = Brand.objects.get_or_create(name=name)
            brands[name.lower()] = brand
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {name}'))

        # Create Categories
        clothing, _ = Category.objects.get_or_create(name="Clothing")
        shoes_cat, _ = Category.objects.get_or_create(name="Shoes")
        
        sub_categories = ["Shirts", "Suits", "Pants"]
        clothing_subs = {}
        for sub in sub_categories:
            cat, created = Category.objects.get_or_create(name=sub, parent=clothing)
            clothing_subs[sub.lower()] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {sub} under Clothing'))

        # Dummy Products Data
        products_data = [
            {"name": "Barba Napoli White Shirt", "brand": "barba napoli", "category": "shirts", "price": 250.00, "color": "White"},
            {"name": "Brunello Cucinelli Navy Suit", "brand": "Brunello Cucinelli", "category": "suits", "price": 3500.00, "color": "Navy"},
            {"name": "Isaia Slim Fit Pants", "brand": "Isaia", "category": "pants", "price": 450.00, "color": "Grey"},
            {"name": "Premiata Leather Sneakers", "brand": "premiata", "category": "shoes", "price": 320.00, "color": "Brown"},
            {"name": "Barba Napoli Linen Shirt", "brand": "barba napoli", "category": "shirts", "price": 280.00, "color": "Blue"},
            {"name": "Brunello Cucinelli Cashmere Pants", "brand": "Brunello Cucinelli", "category": "pants", "price": 850.00, "color": "Beige"},
            {"name": "Isaia Double Breasted Suit", "brand": "Isaia", "category": "suits", "price": 3800.00, "color": "Dark Blue"},
            {"name": "Premiata Classic Shoes", "brand": "premiata", "category": "shoes", "price": 400.00, "color": "Black"},
        ]

        # Use an existing image if available as placeholder
        placeholder_path = 'static/img/landing_hero.png' # Using this as placeholder
        
        for p_info in products_data:
            brand = brands[p_info['brand'].lower()]
            if p_info['category'] == 'shoes':
                category = shoes_cat
            else:
                category = clothing_subs[p_info['category']]
            
            sku = f"{brand.name.replace(' ', '')[:3].upper()}-{p_info['name'].replace(' ', '')[:5].upper()}-{p_info['color'].upper()}"
            
            product, created = Product.objects.get_or_create(
                name=p_info['name'],
                brand=brand,
                category=category,
                defaults={
                    'sku': sku,
                    'price': Decimal(p_info['price']),
                    'color': p_info['color'],
                    'description': f"High quality {p_info['name']} by {brand.name}."
                }
            )
            
            if created:
                # Add sizes
                sizes = ["S", "M", "L", "XL"] if p_info['category'] != 'shoes' else ["41", "42", "43", "44"]
                for size_val in sizes:
                    ProductSize.objects.create(product=product, size=size_val, stock=10)
                
                # Add image placeholder
                if os.path.exists(placeholder_path):
                    with open(placeholder_path, 'rb') as f:
                        img_obj = ProductImage(product=product, is_primary=True)
                        img_obj.image.save(f'product_{product.id}.png', File(f), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded products'))
