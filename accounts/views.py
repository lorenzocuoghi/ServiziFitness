from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ProfileForm, UserForm
from .models import Profile


def register(request):

    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        pf = ProfileForm(request.POST, prefix='profile')
        if uf.is_valid() and pf.is_valid():
            user = uf.save()
            prof = pf.save(commit=False)
            prof.user = user
            prof.save()
            authenticate(username=user.username, password=user.password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        template = 'registration/register.html'
        context = dict(userform=uf, profileform=pf)
        return render(request, template, context)

    else:
        uf = UserForm(prefix='user')
        pf = ProfileForm(prefix='profile')
        template = 'registration/register.html'
        context = dict(userform=uf, profileform=pf)
        return render(request, template, context)


@login_required()
def profile(request):
    prof = Profile.objects.get(user_id__exact=request.user.id)
    template = 'accounts/profile.html'
    context = {'profile': prof}
    return render(request, template, context)
