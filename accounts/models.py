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


class AccountType(models.Model):
    title_account=models.CharField(max_length=100)
    def __str__(self):
        return self.title_account


class Account(models.Model):
    user_account    =models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts_user")
    number_account  =models.CharField(max_length=20, default="")
    type_account    =models.ForeignKey(AccountType, on_delete=models.SET_NULL, blank=True, null=True)
    create_date     =models.DateField(auto_now_add=True)
    ammount         =models.FloatField(default=1000, blank=True, null=True)

    def __str__(self):
        return 'Cuenta {}| Usuario {}'.format(self.id, self.user_account.username)


class ExternAccount(models.Model):
    user_account    =models.ForeignKey(User, on_delete=models.CASCADE, related_name="extern_account_user")
    number_account  =models.CharField(max_length=20)
    nombre_cuenta   =models.CharField(max_length=200, blank=True, null=True)
    limite_diario   =models.IntegerField(blank=True, null=True, default=1000)

    def __str__(self):
        return 'Cuenta Externa enviar {}| Usuario {}'.format(self.id, self.user_account.username)


class Transaction(models.Model):
    user=               models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transaction')
    account=            models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transaction')
    type_transaction=   models.CharField(max_length=100, blank=True, null=True)
    ammount=            models.FloatField(blank=True, null=True) 
    total_account=      models.FloatField(blank=True, null=True)
    reference=          models.CharField(max_length=100, blank=True, null=True)
    transaction_date=   models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return 'Transaction {}| Usuario {}'.format(self.id, self.user.username) 
