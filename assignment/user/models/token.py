from django.db import models


class RefreshToken(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="refresh_tokens"
    )
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
