from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    phone = models.CharField(max_length=215,blank=True)
    address = models.TextField(blank=True,null=True)
    age = models.IntegerField()
