from django.forms import ModelForm
from django import forms
from datetime import date
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms, Email


class AddEventForm(ModelForm):
    portals_cooperating = forms.ModelMultipleChoiceField(
        queryset=Portal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Portale współpracujące')

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
    class Meta:
        model = TaskBeforeEvent
        fields = ['comments']


class TaskAfterForm(ModelForm):
    portal = forms.ModelChoiceField(queryset=None)
    date_when_send = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = TaskAfterEvent
        fields = ['portal', 'send_materials_after_event', 'date_when_send', 'comments']

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)  # 'event' -jest przekazany z widoku w form=Event(..)
        super(TaskAfterForm, self).__init__(*args, **kwargs)
        self.fields['portal'].queryset = event.portals_cooperating.all()  # queryset dla pola formularza


    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        send_materials_after_event = cleaned_data.get('send_materials_after_event')
        date_when_send = cleaned_data.get('date_when_send')
        if date_when_send is not None and send_materials_after_event == False:
            raise forms.ValidationError('Nie zaznaczyłeś, że materiały zostały wysłane!')


class EventAddPortalForm(forms.Form):
    portal = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=Portal.objects.all(), label='Portale')


class EventUpdateForm(forms.Form):
    event = forms.CharField(label='Tytuł wydarzenia')
    date = forms.DateField(label='data')


class EventRemovePortalForm(forms.Form):
    """Form that is used for deleting portals from choosen event"""
    portals_cooperating = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=None)

    class Meta:
        model = Event
        fields = ['portals_cooperating']

    def __init__(self, *args, **kwargs):
        """overriding __init__ function form changing queryset for form's field - portal_cooperating
        field, this field should have only portals that were assigned to that event
        not every portal in the database"""
        event = kwargs.pop('event', None) #'event' -jest przekazany z widoku w form=Event(..)
        super(EventRemovePortalForm, self).__init__(*args, **kwargs)
        self.fields['portals_cooperating'].queryset = event.portals_cooperating.all() #queryset dla pola formularza


class CooperationTermsForm(ModelForm):
    portal = forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect)

    class Meta:
        model = CooperationTerms
        fields = ['portal', 'services_for_portal', 'services_provided_by_portal', 'comments']


    def __init__(self, *args, **kwargs):
        """overriding __init__ function -changing queryset for form's field - portal
                field, this field should have only portals that were assigned to that event
                not every portal in the database"""
        event = kwargs.pop('event', None) #'event' -jest przekazany z widoku w form=Event(..)
        super(CooperationTermsForm, self).__init__(*args, **kwargs)
        self.fields['portal'].queryset = event.portals_cooperating.all() #queryset dla pola formularza






