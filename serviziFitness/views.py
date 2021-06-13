from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return HttpResponseRedirect(reverse('workout:index'))


def logout_view(request):
    """Log users out and re-direct them to the main page."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))
