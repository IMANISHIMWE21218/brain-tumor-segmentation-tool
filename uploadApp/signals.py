from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Patient


@receiver(post_save, sender=Patient)
def ml_conversion(sender, instance, created, **kwargs):
    print()
    print()
    print("happening...")
    print()
    print()
