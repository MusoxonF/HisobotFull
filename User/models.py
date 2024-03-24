from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class User(AbstractUser):
    JINS = [
            ('Erkak', 'Erkak'),
            ('Ayol', 'Ayol'),
            ('Null', 'Null'),
        ]
    is_admin = models.BooleanField(default=False)
    is_direktor = models.BooleanField(default=False)
    is_xodim = models.BooleanField(default=True)
    is_bulim = models.BooleanField(default=False)
    is_tekshiruvchi = models.BooleanField(default=False)
    gender = models.CharField(max_length=6, choices = JINS, default='Null')
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.ImageField(upload_to = 'user_photos', default='default.jpg')

    def __str__(self):
        return self.username


class Ish_turi(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ish_id = models.CharField(max_length = 5, unique=True)
    def __str__(self):
        return self.name


class Bolim(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bulim_id = models.CharField(max_length = 5, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}/{self.user}'


class Xodim(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="xodim_user", null=True)
    ish_turi = models.ManyToManyField(Ish_turi, related_name = 'ish_turi')
    bulimi = models.ForeignKey(Bolim, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'bolim')
    def __str__(self):
        return f'{self.user.username}/{self.user.first_name}'
    

@receiver(post_save, sender=User)
def create_xodim(sender, instance, created=False, **kwargs):
    if created:
        if instance.is_xodim==True:
            xodim = Xodim.objects.create(user=instance)
            return xodim
        else:
            return False
    else:
            return False