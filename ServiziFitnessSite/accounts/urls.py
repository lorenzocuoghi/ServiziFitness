from django.urls import path

from . import api, views

app_name = 'accounts'

urlpatterns = [
    path('api/profile/<int:pk>/', api.ProfileDetail.as_view(), name='profile_api'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.edit, name='edit'),
    path('profile/submit', views.submit, name='submit'),
    path('register/', views.register, name='register'),
]
