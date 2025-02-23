from django.contrib import admin
from .models import *

class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields=('sender','conversation','body')

# Register your models here.
admin.site.register(InboxMessage,InboxMessageAdmin)
admin.site.register(Conversation)
