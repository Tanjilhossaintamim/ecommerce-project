from django.conf import settings
from .models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_new_customer(sender,**kwargs):
    if kwargs['created']:
        return Customer.objects.create(user=kwargs['instance'])