from django.forms import ModelForm
from django import forms


from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date']

class AddPortalForm(ModelForm):
    class Meta:
        model = Portal
        fields = ['name', 'category', 'address', 'email', 'logotype', 'comments']


class AddPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'portal', 'comments']

class SearchForm(forms.Form):
    search = forms.CharField(label='Szukaj')