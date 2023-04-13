from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import *
# Register your models here.


class StockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            ('<15', 'low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<15':
            return queryset.filter(stock__lt=15)


@admin.register(Collection)
class CollecitonAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    list_per_page = 10
    search_fields = ['title']

    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection_id': str(collection.id)}))
        return format_html(f'<a href="{url}">{collection.product_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('products'))


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['thambnail']

    def thambnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" id="thambnail"/>')
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock_status', 'collection']
    list_editable = ['price']
    list_per_page = 10
    list_filter = ['last_update', StockFilter]
    list_select_related = ['collection']
    ordering = ['title']
    actions = ['clear_stock']
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }

    def __str__(self) -> str:
        return self.title

    def stock_status(self, product):
        if product.stock > 15:
            return 'ok'
        return 'low'

    @admin.action(description='Clear Stock')
    def clear_stock(self, request, queryset):
        update = queryset.update(stock=0)
        return self.message_user(request, f'update successfully')

    class Media:
        css = {
            'all': ['store/style.css']
        }


class OrderInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['id', 'payment_status', 'placed_at', 'customer']
    list_filter = ['placed_at', 'payment_status']
    list_per_page = 10
    inlines = [OrderInline]
    autocomplete_fields = ['customer']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    actions = ['change_membership']
    search_fields = ['user__first_name__istartswith']

    def order_count(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({'customer_id': str(customer.id)}))
        return format_html(f'<a href="{url}">{customer.order_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('orders'))

    @admin.action(description='change membership bronze')
    def change_membership(self, request, queryset):
        update = queryset.update(membership='b')
        return self.message_user(request, f'membership update successfully')
