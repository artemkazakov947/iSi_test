from django.conf import settings
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thread id {self.id}"

    class Meta:
        ordering = ["-updated"]


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
