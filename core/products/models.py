from django.db import models


class Brand(models.Model):
    """The fashion brand/designer - e.g. Kiton, Isaia, Brunello Cucinelli"""
    name = models.CharField(max_length=100)# The brand name shown on the site e.g. "Kiton"
    def __str__(self):
        return self.name


class Category(models.Model):
    """Product category - e.g. Suits, Blazers, Shoes, Accessories"""
    name = models.CharField(max_length=100)# Category name e.g. "Suits", "Sneakers", "Sweaters"
    def __str__(self):
        return self.name


class Product(models.Model):
    """A single product listed on the store"""
    name = models.CharField(max_length=255)# Full product name e.g. "Kiton Black Cashmere Sneakers"
    description = models.TextField(blank=True)# Long product description shown on the product page
    sku = models.CharField(max_length=100, unique=True)# Unique product code from the brand e.g. "USSFITBN008474000S"
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)# Which brand makes this product e.g. Kiton, Isaia
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)# Which category it belongs to e.g. Shoes, Suits
    price = models.DecimalField(max_digits=10, decimal_places=2)# Current selling price e.g. 770.00 (EUR)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)# Price before discount - shows as strikethrough on the site
    color = models.CharField(max_length=100, blank=True)# Color of the item e.g. "Black", "Dark Blue", "Brown"
    is_on_sale = models.BooleanField(default=False)# If True, product is discounted
    created_at = models.DateTimeField(auto_now_add=True)# When this product was added to the database
    updated_at = models.DateTimeField(auto_now=True)# Last time this product was edited
    def __str__(self):
        return self.name

    def get_primary_image(self):
        """Returns the image marked as primary, or the first one available if none are marked."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()


class ProductSize(models.Model):
    """Available sizes for a product with stock count"""
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')# Which product this size belongs to
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)# Restricted to S, M, L, XL
    stock = models.PositiveIntegerField(default=0)# How many units are available for this size
    def __str__(self):
        return f"{self.product.name} - {self.size}"


class ProductImage(models.Model):
    """Images for a product - each product can have multiple photos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')# Which product this image belongs to
    image = models.ImageField(upload_to='public/')# The actual photo file
    is_primary = models.BooleanField(default=False)# The main image shown in product listing cards
    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    """Shopping cart attached to a session"""
    session_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    """Item inside a shopping cart"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, default='M') # Default added for existing rows
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity