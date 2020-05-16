from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class IndividualWallet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    value = models.FloatField(null=True)
    slug = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(IndividualWallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class IndividualTransactions(models.Model):
    wallet = models.ForeignKey(
        IndividualWallet,
        on_delete=models.CASCADE,
    )
    date = models.DateField(null=True)
    transaction_type = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)

class Clan(models.Model):
    name = models.CharField(max_length=200)
    public = models.BooleanField()
    members = models.ManyToManyField(User)
    slug = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Clan, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ClanWallet(models.Model):
    name = models.CharField(max_length=200)
    clan = models.ForeignKey(
        Clan,
        on_delete=models.CASCADE,
    )
    value = models.FloatField(null=True)
    have_target = models.BooleanField()
    target = models.FloatField(null=True)
    percent = models.FloatField(null=True)
    slug = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.have_target:
            self.percent = (self.value / self.target) * 100
        super(ClanWallet, self).save(*args, **kwargs)

class ClanWalletAdmin(models.Model):
    clanwallet = models.ForeignKey(
        ClanWallet,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
