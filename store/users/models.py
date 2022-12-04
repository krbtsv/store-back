from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_photos/%Y/%m/%d/', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        db_table = 'email_verification'
        verbose_name = 'Подтверждение адреса электронной почты'
        verbose_name_plural = 'Подтверждение адреса электронной почты'

    def send_verification_email(self):
        send_mail(
            'Subject here',
            'Test verification email',
            'from@example.com',
            [self.user.email],
            fail_silently=False,
        )

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
