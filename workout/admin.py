from django.contrib import admin
from .models import ConcreteExercise, Exercise, TrainingCard


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Details', {'fields': ['image_tag', 'image', 'description', 'type', 'level']}),
        ('Visibility', {'fields': ['public'], 'classes': ['collapse']}),
    ]
    readonly_fields = ['image_tag']
    list_display = ['name', 'type', 'level', 'public']
    list_filter = ['type', 'level', 'public']
    search_fields = ['name']
    radio_fields = {'level': admin.VERTICAL}


class ExerciseInline(admin.StackedInline):
    model = ConcreteExercise
    extra = 1


@admin.register(TrainingCard)
class TrainingCardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Details', {'fields': ['description', 'type', 'level', 'goal', 'taw']}),
        ('Visibility', {'fields': ['public'], 'classes': ['collapse']}),
    ]
    inlines = [ExerciseInline]
    list_display = ['name', 'type', 'level', 'public', 'goal', 'taw']
    list_filter = ['type', 'level', 'public']
    search_fields = ['name']
