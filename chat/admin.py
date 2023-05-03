from django.contrib import admin

from chat.models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "updated"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["thread", "created"]
    readonly_fields = ("thread", "sender", "is_read", "text")
    list_filter = ("is_read", )
