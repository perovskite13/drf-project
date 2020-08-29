from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

# Create your models here.
class Echo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    category = models.ForeignKey(
        'EchoCategory',
        on_delete=models.CASCADE,
        related_name='category_projects',
        null=True,
        blank=True
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length = 200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Echo',
        on_delete=models.CASCADE,
        related_name = 'pledges'
    )   
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )

class EchoCategory(models.Model):
    name = models.CharField(max_length=200)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )