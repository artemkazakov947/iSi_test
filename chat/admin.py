from django.contrib import admin

from chat.models import Thread, Message

admin.site.register(Thread)
admin.site.register(Message)
