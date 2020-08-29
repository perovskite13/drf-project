from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio=models.TextField(blank=True,null=True)
    location=models.CharField(max_length=30,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=False)
    is_mentor=models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class userProfile(models.Model):
#     user=models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name="profile")
