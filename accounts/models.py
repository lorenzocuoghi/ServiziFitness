from django.contrib.auth.models import User
from django.db import models

SEX_CHOICES = (('M', 'Male',), ('F', 'Female',))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birthday = models.DateField()
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    @staticmethod
    def get_field_names(self):
        names = [field.name for field in self._meta.fields]
        names.remove('id')
        names.remove('user')
        return names
