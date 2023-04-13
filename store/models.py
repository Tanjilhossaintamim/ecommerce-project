from uuid import uuid4
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator
from .validators import file_size_validator

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    last_update = models.DateField(auto_now_add=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images',
                              validators=[file_size_validator])
    
    


class Customer(models.Model):
    bronze = 'b'
    silver = 's'
    gold = 'g'
    choice = [
        (bronze, 'bronze'),
        (silver, 'silver'),
        (gold, 'gold')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=choice, default=bronze)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__firs_name')
    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    payment_panding = 'p'
    payment_compleate = 'c'
    payment_failed = 'f'
    payment_choice = [
        (payment_panding, 'panding'),
        (payment_compleate, 'compleate'),
        (payment_failed, 'failed')
    ]
    payment_status = models.CharField(
        max_length=1, choices=payment_choice, default=payment_panding)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    create_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])


class Review(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
