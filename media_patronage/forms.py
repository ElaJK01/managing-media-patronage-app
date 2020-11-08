from django.forms import ModelForm
from django import forms
from datetime import date
from django.forms.widgets import CheckboxSelectMultiple
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms, Email


class AddEventForm(ModelForm):
    portals_cooperating = forms.ModelMultipleChoiceField(
        queryset=Portal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    label= 'Portale współpracujące')

    class Meta:
        model = Event
        fields = ['title', 'date', 'portals_cooperating']


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


class TaskBeforeForm(ModelForm):
    when_send_invitation = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = TaskBeforeEvent
        fields = ['send_invitation_to_portals', 'when_send_invitation', 'comments']




class TaskAfterForm(ModelForm):
    class Meta:
        model = TaskAfterEvent
        fields = ['event', 'portal', 'send_materials_after_event', 'date_when_send', 'comments']


