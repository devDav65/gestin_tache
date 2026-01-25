from django.db import models
from django.contrib.auth.models import User

    
# class User(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     email = models.EmailField(max_length=254)
    
#     def __str__(self):
#         return self.username
# Create your models here.
class Task(models.Model):
    titre = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    date_creation = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    proprio = models.ForeignKey(User,related_name='task', on_delete=models.CASCADE)
    def __str__(self):
        return self.titre
