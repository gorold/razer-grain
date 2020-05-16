from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,

    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    nric = models.CharField(max_length=9, verbose_name="NRIC")
    date_of_birth = models.DateField(null=True, verbose_name="Date of Birth")
    country = CountryField()
    

class IndividualWallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    value = models.FloatField(null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        IndividualWallet.objects.create(user=instance)
    instance.profile.save()
    instance.individualwallet.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.individualwallet.save()

class Guild(models.Model):
    guild_name = models.CharField(max_length=200)

class GuildWallet(models.Model):
    wallet_name = models.CharField(max_length=200)
    guild = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
    )

