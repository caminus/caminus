import models
from django.contrib import admin

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'balance')
    search_fields = ('profile__mc_username',)

class InviteAdmin(admin.ModelAdmin):
    list_display = ('code', 'creator', 'claimer', 'deleted')
    search_fields = ('code', 'creator', 'claimer')
    list_filter = ('deleted',)

admin.site.register(models.CurrencyAccount, CurrencyAdmin)
admin.site.register(models.Quote)
admin.site.register(models.Invite, InviteAdmin)
