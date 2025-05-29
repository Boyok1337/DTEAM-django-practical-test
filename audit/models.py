from django.db import models
from django.conf import settings

from base.models import BaseModel

User = settings.AUTH_USER_MODEL


class RequestLog(BaseModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=2048)
    query_string = models.TextField(blank=True, null=True)
    remote_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.timestamp} {self.method} {self.path}"
