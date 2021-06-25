from rest_framework.serializers import ModelSerializer

from .models import Exercise, TrainingCard


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class TrainingCardSerializer(ModelSerializer):
    class Meta:
        model = TrainingCard
        fields = '__all__'
