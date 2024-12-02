# myapp/models.py
from django.db import models

class Logo(models.Model):
    image = models.ImageField(upload_to='logo/')


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name