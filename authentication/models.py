from django.db import models
from django.contrib.auth.models import User

class ACModel(models.Model):
    articleid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(null=True, max_length=150)
    author = models.CharField(null=True, max_length=50)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=False)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    date_time = models.DateTimeField()

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
