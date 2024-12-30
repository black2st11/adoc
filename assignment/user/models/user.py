from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    hashed_password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        