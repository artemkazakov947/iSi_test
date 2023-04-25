from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Thread(models.Model):
    participants = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thread for {self.participants}. Updated: {self.updated}"

    class Meta:
        ordering = ["-updated"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.participants.count() > 2:
            raise ValidationError("Thread can not have more then 2 participant")
        return super(Thread, self).save(force_insert, force_update, using, update_fields)


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender}, created: {self.created}"

    class Meta:
        ordering = ["-is_read"]
