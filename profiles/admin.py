import models
from django.contrib import admin

class InviteAdmin(admin.ModelAdmin):
    list_display = ('code', 'creator', 'claimer', 'deleted')
    search_fields = ('code', 'creator', 'claimer')
    list_filter = ('deleted',)

admin.site.register(models.Invite, InviteAdmin)
