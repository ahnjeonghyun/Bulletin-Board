from django.db import models

class User(models.Model):
    nickname        = models.CharField(max_length=100)
    password        = models.CharField(max_length=200)
    content         = models.TextField()
    head            = models.CharField(max_length=300)
    hits            = models.IntegerField(default=0)
    create_at       = models.DateTimeField(auto_now_add=True)
    secret_is       = models.BooleanField(default=False)
    tag             = models.CharField(max_length=300,null=True)
    admin_is_answer = models.BooleanField(default=False)
    admin_answer    = models.OneToOneField('admins.Admin', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'users'