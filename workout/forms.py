from django import forms
from django.utils.html import mark_safe

from .models import Exercise, TrainingCard


class ImagePreviewWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            input_html = input_html.split('</a>')[1]
            img_html = mark_safe(f'<img src="{value.url}"/>')
        else:
            img_html = mark_safe(f'<img src="" alt="No image"/><br>')
        return f'{img_html}{input_html}'


class ExerciseForm(forms.ModelForm):
    image = forms.ImageField(max_length=500, required=False, widget=ImagePreviewWidget)

    class Meta:
        model = Exercise
        exclude = ('id', 'user',)


class TrainingCardForm(forms.ModelForm):

    class Meta:
        model = TrainingCard
        exclude = ('id', 'user', 'exercises')
