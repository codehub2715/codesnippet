from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    model = models.CharField(max_length=64)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user or 'Anonymous'}: {self.prompt[:30]}... ({self.created_at:%Y-%m-%d %H:%M})"
