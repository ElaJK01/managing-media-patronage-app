from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import FormView
from .forms import AddEventForm
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms


class EventList(ListView):
    model = Event

class AddEvent(FormView):
    template_name = "event_form.html"
    form_class = AddEventForm
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)