from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, FormView

from .forms import ExerciseForm, TrainingCardForm
from .models import Exercise, TrainingCard, ConcreteExercise


def index(request):
    template = 'workout/index.html'
    return render(request, template)


@method_decorator(login_required, name='dispatch')
class TrainingCardView(ListView):

    def get_queryset(self):
        return TrainingCard.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ExerciseView(ListView):

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)


# --------------------------------------------------------------------------------------------------------------


@login_required
def trainingcard_create(request):
    ExerciseFormSet = inlineformset_factory(TrainingCard, ConcreteExercise, extra=1, exclude=('id', 'card',))
    queryset = Exercise.objects.filter(Q(user=request.user) | Q(public__exact=True))
    if request.method == 'POST':
        form = TrainingCardForm(request.POST)
        form.instance.user = request.user
        card = form.save(commit=False)
        exer_formset = ExerciseFormSet(request.POST, instance=card)
        if form.is_valid() and exer_formset.is_valid():
            card = form.save()
            exer_formset.save()
            return HttpResponseRedirect(reverse('workout:trainingcard_detail', args=(card.id,)))
    else:
        form = TrainingCardForm()
        exer_formset = ExerciseFormSet()
        exer_formset.form.base_fields['exercise'].queryset = queryset
    template = 'workout/trainingcard_form.html'
    context = {'form': form, 'exer_formset': exer_formset}
    return render(request, template, context)


class TrainingCardDetailView(DetailView):
    model = TrainingCard


@login_required
def trainingcard_change(request, card_id):
    ExerciseFormSet = inlineformset_factory(TrainingCard, ConcreteExercise, extra=1, exclude=('id', 'card',))
    queryset = Exercise.objects.filter(Q(user=request.user) | Q(public__exact=True))
    card = get_object_or_404(TrainingCard, pk=card_id)
    form = TrainingCardForm(instance=card)
    exer_formset = ExerciseFormSet(instance=card)
    exer_formset.form.base_fields['exercise'].queryset = queryset
    template = 'workout/trainingcard_form.html'
    context = {'card_id': card_id, 'form': form, 'exer_formset': exer_formset}
    return render(request, template, context)


@login_required
def trainingcard_submit(request, card_id):
    ExerciseFormSet = inlineformset_factory(TrainingCard, ConcreteExercise, extra=1, exclude=('id', 'card',))
    card = get_object_or_404(TrainingCard, pk=card_id)
    form = TrainingCardForm(request.POST, instance=card)
    exer_formset = ExerciseFormSet(request.POST, instance=card)
    if form.is_valid() and exer_formset.is_valid():
        form.save()
        exer_formset.save()
        return HttpResponseRedirect(reverse('workout:trainingcard_detail', args=(card.id,)))
    else:
        template = 'workout/trainingcard_form.html'
        context = {'card_id': card_id, 'form': form, 'exer_formset': exer_formset}
        return render(request, template, context)


def trainingcard_search(request):
    trainingcard_list = TrainingCard.objects.filter(public__exact=True)
    search = True
    context = {'trainingcard_list': trainingcard_list, 'search': search}
    template = 'workout/trainingcard_list.html'
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class TrainingCardDeleteView(DeleteView):
    model = TrainingCard
    success_url = reverse_lazy('workout:trainingcard_list')


# --------------------------------------------------------------------------------------------------------------


@method_decorator(login_required, name='dispatch')
class ExerciseCreateView(FormView):
    template_name = 'workout/exercise_form.html'
    form_class = ExerciseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        exer = form.save()
        return HttpResponseRedirect(reverse('workout:exercise_detail', args=(exer.id, )))


class ExerciseDetailView(DetailView):
    model = Exercise


@login_required
def exercise_change(request, exer_id):
    exer = get_object_or_404(Exercise, pk=exer_id)
    form = ExerciseForm(instance=exer)
    template = 'workout/exercise_form.html'
    context = {'exer_id': exer_id, 'form': form}
    return render(request, template, context)


@login_required
def exercise_submit(request, exer_id):
    exer = get_object_or_404(Exercise, pk=exer_id)
    form = ExerciseForm(request.POST, request.FILES, instance=exer)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('workout:exercise_detail', args=(exer.id,)))
    else:
        template = 'workout/exercise_form.html'
        context = {'exer_id': exer_id, 'form': form}
        return render(request, template, context)


def exercise_search(request):
    exercise_list = Exercise.objects.filter(public__exact=True)
    search = True
    context = {'exercise_list': exercise_list, 'search': search}
    template = 'workout/exercise_list.html'
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class ExerciseDeleteView(DeleteView):
    model = Exercise
    success_url = reverse_lazy('workout:exercise_list')
