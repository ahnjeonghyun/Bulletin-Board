from django.db import models

class User(models.Model):
    nickname        = models.CharField(max_length=100)
    password        = models.CharField(max_length=300,null=True)
    content         = models.TextField()
    title           = models.CharField(max_length=300)
    hits            = models.IntegerField(default=0)
    create_at       = models.DateTimeField(auto_now_add=True)
    secret_is       = models.BooleanField(default=False)
    tag             = models.CharField(max_length=300,null=True)
    admin_is_answer = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'