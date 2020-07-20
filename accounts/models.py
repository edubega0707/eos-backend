from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    usuario     =models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_usuario")
    telefono    =models.CharField(max_length=15, blank=True, null=True)
    domicilio   =models.CharField(max_length=300, blank=True, null=True)
    foto        =models.URLField(blank=True, null=True)

    def __str__(self):
        return self.usuario.username

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(usuario=kwargs.get('instance'))
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)