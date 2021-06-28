from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Exercise, TrainingCard
from .serializers import ExerciseSerializer, TrainingCardSerializer


class ExerciseViewSet(ModelViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)


class TrainingCardViewSet(ModelViewSet):
    serializer_class = TrainingCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TrainingCard.objects.filter(user=self.request.user)


class ExerciseSearchViewSet(ReadOnlyModelViewSet):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.filter(public__exact=True)


class TrainingCardSearchViewSet(ReadOnlyModelViewSet):
    serializer_class = TrainingCardSerializer

    def get_queryset(self):
        return TrainingCard.objects.filter(public__exact=True)
