from django import forms
from django.utils.html import mark_safe

from .models import Exercise, LEVEL_CHOICES, TrainingCard


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
    level = forms.CharField(max_length=15, widget=forms.RadioSelect(choices=LEVEL_CHOICES))

    class Meta:
        model = Exercise
        fields = model.get_field_names(model)


class TrainingCardForm(forms.ModelForm):
    level = forms.CharField(max_length=15, widget=forms.RadioSelect(choices=LEVEL_CHOICES))

    class Meta:
        model = TrainingCard
        fields = model.get_field_names(model)
