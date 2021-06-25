from django.urls import include, path
from rest_framework import routers

from . import api, views

app_name = 'workout'

router = routers.DefaultRouter()
router.register(r'api/exercise/search', api.ExerciseSearchViewSet, 'exercise_search_api')
router.register(r'api/trainingcard/search', api.TrainingCardSearchViewSet, 'trainingcard_search_api')
router.register(r'api/exercise', api.ExerciseViewSet, 'exercise_api')
router.register(r'api/trainingcard', api.TrainingCardViewSet, 'trainingcard_api')

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
    path('trainingcard/', views.TrainingCardView.as_view(), name='trainingcard_list'),
    path('trainingcard/create/', views.trainingcard_create, name='trainingcard_create'),
    path('trainingcard/<int:pk>/', views.TrainingCardDetailView.as_view(), name='trainingcard_detail'),
    path('trainingcard/<int:card_id>/change/', views.trainingcard_change, name='trainingcard_change'),
    path('trainingcard/<int:card_id>/submit/', views.trainingcard_submit, name='trainingcard_submit'),
    path('trainingcard/<int:pk>/delete/', views.TrainingCardDeleteView.as_view(), name='trainingcard_delete'),
    path('trainingcard/search/', views.trainingcard_search, name='trainingcard_search'),
    path('exercise/', views.ExerciseView.as_view(), name='exercise_list'),
    path('exercise/create/', views.ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercise/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/<int:exer_id>/change/', views.exercise_change, name='exercise_change'),
    path('exercise/<int:exer_id>/submit/', views.exercise_submit, name='exercise_submit'),
    path('exercise/<int:pk>/delete/', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
    path('exercise/search/', views.exercise_search, name='exercise_search'),
]
