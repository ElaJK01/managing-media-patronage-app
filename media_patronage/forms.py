from django.forms import ModelForm

from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date']
