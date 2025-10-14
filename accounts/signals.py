from django.db.models.signals import post_delete, pre_delete,post_save
from .models import User, UserProfile
from django.dispatch import receiver


@receiver(post_save, sender = User)
def create_user_profile(sender , instance, created, **kwargs):
    UserProfile.objects.create(user = instance)
    print(f"profile created for {instance.username}")
    