from django.contrib.auth.models import User
from django.db import models

SEX_CHOICES = (('M', 'Male',), ('F', 'Female',))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birthday = models.DateField()
    height = models.PositiveSmallIntegerField('Height (cm)', blank=True, null=True)
    weight = models.PositiveSmallIntegerField('Weight (Kg)', blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
