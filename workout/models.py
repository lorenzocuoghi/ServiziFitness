import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.html import mark_safe
from PIL import Image
from uuid import uuid4

LEVEL_CHOICES = (('UNIQUE', 'Unique'), ('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'),
                 ('ADVANCED', 'Advanced'))
CARD_TYPE_CHOICES = (('FULL_BODY', 'Full Body'), ('UPPER_BODY', 'Upper Body'), ('LOWER_BODY', 'Lower Body'),
                     ('PUSH', 'Push'), ('PULL', 'Pull'), ('LEGS', 'Legs'))
EXER_TYPE_CHOICES = (('WARM-UP', 'Warm-up'), ('CARDIO', 'Cardio'), ('ARMS', 'Arms'), ('CHEST', 'Chest'),
                     ('SHOULDERS', 'Shoulders'), ('CORE', 'Core'), ('BACK', 'Back'), ('LEGS', 'Legs'),
                     ('STRETCHING', 'Stretching'))
GOAL_CHOICES = (('MASS', 'Mass'), ('RESISTANCE', 'Resistance'), ('TONE', 'Tone'), ('FAT-BURNING', 'Fat-Burning'))
TOOL_CHOICES = (('FREEBODY', 'Freebody'), ('LOOP_BAND', 'Loop band'), ('PULL_UP_BAR', 'Pull-up bar'),
                ('PARALLEL_BARS', 'Parallel bars'), ('DUMBBELLS', 'Dumbbells'), ('BARBELL', 'Barbell'))


def rename(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    from .urls import app_name
    savepath = os.path.join(settings.MEDIA_ROOT, app_name)
    savepath = os.path.join(savepath, 'exercise')
    return os.path.join(savepath, filename)


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200, blank=True, default="Suggestions...\nCommon errors...")
    type = models.CharField(max_length=15, choices=EXER_TYPE_CHOICES, default=EXER_TYPE_CHOICES[0])
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default=LEVEL_CHOICES[0])
    tool = models.CharField(max_length=15, choices=TOOL_CHOICES, default=TOOL_CHOICES[0])
    image = models.ImageField(upload_to=rename, max_length=500, blank=True, default=None)
    video = models.URLField('Video tutorial', max_length=128, blank=True)
    public = models.BooleanField(default=False)

    def image_tag(self):
        return mark_safe('<img src="{}" />'.format(self.image.url))
    image_tag.short_description = 'Thumbnail'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return str(self.name + ' (by ' + self.user.username + ')')

    class Meta:
        unique_together = (('name', 'user'),)


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Exercise)
def auto_delete_file_on_delete(instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Exercise` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Exercise)
def auto_delete_file_on_change(instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Exercise` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = Exercise.objects.get(pk=instance.pk).image
    except Exercise.DoesNotExist:
        return False

    if not old_image:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


class TrainingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300, blank=True)
    type = models.CharField(max_length=15, choices=CARD_TYPE_CHOICES, default=CARD_TYPE_CHOICES[0])
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default=LEVEL_CHOICES[0])
    goal = models.CharField(max_length=15, choices=GOAL_CHOICES, default=GOAL_CHOICES[0])
    taw = models.PositiveSmallIntegerField('Times a week', default=0)
    duration = models.PositiveSmallIntegerField('Duration (minutes)', default=0)
    public = models.BooleanField(default=False)
    exercises = models.ManyToManyField(Exercise, through='ConcreteExercise')

    class Meta:
        unique_together = (('name', 'user'),)

    def __str__(self):
        return str(self.name + ' (by ' + self.user.username + ')')


class ConcreteExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    card = models.ForeignKey(TrainingCard, on_delete=models.CASCADE)
    series = models.PositiveSmallIntegerField(default=0)
    reps = models.PositiveSmallIntegerField(default=0)
    weight = models.FloatField('Weight (if any) [Kg]', default=0)
    rest = models.PositiveSmallIntegerField("Rest (seconds)", default=0)

    def __str__(self):
        return self.exercise.name
