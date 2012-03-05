import models
from django.contrib import admin

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'balance')
    search_fields = ('profile__mc_username',)

admin.site.register(models.CurrencyAccount, CurrencyAdmin)
admin.site.register(models.Quote)
