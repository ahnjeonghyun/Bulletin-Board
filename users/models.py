from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=45)
    password   = models.CharField(max_length=300)
    email      = models.CharField(max_length=255)
    nickname   = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'