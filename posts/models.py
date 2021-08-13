from django.db import models

class Post(models.Model):
    group_id     = models.BigIntegerField(default=0)
    group_order  = models.IntegerField(default=0)
    group_indent = models.IntegerField(default=0)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title        = models.CharField(max_length=300)
    content      = models.TextField()
    hits         = models.BigIntegerField(default=0)
    tags         = models.CharField(max_length=400,null=True)
    password     = models.CharField(max_length=300)
    created_at   = models.DateField(auto_now_add=True)
    secret_is    = models.BooleanField()

    class Meta:
        db_table = 'posts'

class File(models.Model):
    post     = models.OneToOneField('Post', on_delete=models.CASCADE)
    file_url = models.URLField(max_length=255)

    class Meta:
        db_table = 'files'