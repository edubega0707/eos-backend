from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Profile, Account, AccountType, Transaction

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('id','telefono','domicilio', 'foto', 'usuario')
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_account', 'create_date', 'type_account','ammount')
class AccountTypeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_account')
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','account','ammount','reference','transaction_date')



admin.site.register(Profile,ProfileModelAdmin)
admin.site.register(Account,AccountModelAdmin)
admin.site.register(AccountType,AccountTypeModelAdmin)
admin.site.register(Transaction,TransactionModelAdmin)