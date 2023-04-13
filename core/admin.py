from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasedUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product, ProductImage
from tags.models import TaggedItem
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(BasedUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'first_name', 'last_name'),
            },
        ),
    )


class Taginline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ['tag']




class CustomProductAdmin(ProductAdmin):
    inlines = [Taginline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
