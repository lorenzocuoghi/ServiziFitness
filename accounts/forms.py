from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, SEX_CHOICES


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    sex = forms.CharField(max_length=1, widget=forms.RadioSelect(choices=SEX_CHOICES))

    class Meta:
        model = Profile
        fields = Profile.get_field_names(Profile)
        widgets = {'birthday': DateInput()}
