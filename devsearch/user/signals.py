from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.conf import settings
from . models import Profile


#@receiver(post_save, sender=User)   #another way to do post_save.connect() by using decorator
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            name = user.first_name,
            email = user.email,
        )
        
        subject='Welcome to DevSearch'
        message='We are glad, You are here!'
        sender = settings.EMAIL_HOST_USER
        recipient = [profile.email]
        send_mail(subject, message, sender, recipient, fail_silently=False)
        
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

    
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)