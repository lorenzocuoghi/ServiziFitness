from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ProfileForm, UserEditForm, UserForm


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
    template = 'accounts/profile.html'
    context = {'profile': request.user.profile}
    return render(request, template, context)


@login_required()
def edit(request):
    uf = UserEditForm(prefix='user', instance=request.user)
    pf = ProfileForm(prefix='profile', instance=request.user.profile)
    template = 'registration/register.html'
    context = dict(userform=uf, profileform=pf)
    return render(request, template, context)


@login_required()
def submit(request):
    uf = UserEditForm(request.POST, prefix='user', instance=request.user)
    pf = ProfileForm(request.POST, prefix='profile', instance=request.user.profile)
    if uf.is_valid() and pf.is_valid():
        uf.save()
        pf.save()
        return HttpResponseRedirect(reverse('accounts:profile'))
    return HttpResponseRedirect(reverse('accounts:edit'))
