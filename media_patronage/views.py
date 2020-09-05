from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
# from django.core.files.storage import FileSystemStorage
from .forms import AddEventForm, AddPortalForm, AddPersonForm, SearchForm
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms
from django.db.models import Q


class EventList(ListView):
    model = Event


class AddEvent(FormView):
    template_name = "event_form.html"
    form_class = AddEventForm
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EventDetailsView(DetailView):
    model = Event

#FIXME Dopisać informacje o zadaniach przed i po wydarzeniu

class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')
    template_name = 'event_delete.html'



class EventUpdateView(View):
    def get(self, request, pk):
        event_to_update = Event.objects.get(pk=pk)
        if event_to_update:
            ctx = {'event': event_to_update}
            return render(request, 'event_update.html', ctx)
        else:
            msg = {'msg': 'Nie ma takiego wydarzenia!'}
            return render(request, 'event_update.html', msg)

    def post(self, request, pk):
        event_to_update = Event.objects.get(pk=pk)
        portal= request.POST.get('portal')
        portal_to_add = Portal.objects.get(name=portal)
        event_to_update.portals_cooperating.add(portal_to_add)
        event_to_update.save()
        return redirect(f'/event_details/{event_to_update.pk}')


class PortalList(ListView):
    model = Portal


class SearchFormView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        if self.request.GET:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                search_que = form.cleaned_data['search']
                portals = Portal.objects.filter(Q(name__icontains = search_que)|Q(category__icontains = search_que)\
                                             | Q(address__icontains = search_que) |Q(email__icontains=search_que))
                persons = Person.objects.filter(Q(first_name__icontains = search_que) | Q(last_name__icontains=search_que))
                result_portal = [portal for portal in portals]
                result_person = [person for person in persons]
                result = result_portal+result_person
            else:
                result = []
        else:
            form = SearchForm()
            result = None
        ctx = {"result": result,
               "form": form}
        return ctx


class PersonList(ListView):
    model = Person


class AddPortal(CreateView):
    template_name = 'portal_form.html'
    form_class = AddPortalForm
    success_url = reverse_lazy("portal_list")


class AddPerson(CreateView):
    template_name = 'person_form.html'
    model = Person
    fields = '__all__'
    success_url = reverse_lazy("person_list")


class PersonDetailView(DetailView):
    model = Person


class PersonUpdateView(UpdateView):
    model = Person
    fields = '__all__'
    success_url = reverse_lazy('person_list')
    template_name = 'person_form.html'


class PersonDeleteView(DeleteView):
    model = Person
    success_url = reverse_lazy('person_list')
    template_name = 'person_delete.html'


class PortalUpdateView(UpdateView):
    model = Portal
    fields = '__all__'
    success_url = reverse_lazy('portal_list')
    template_name = 'portal_form.html'


class PortalDetailView(DetailView):
    model = Portal


class PortalDeleteView(DeleteView):
    model = Portal
    success_url = reverse_lazy('portal_list')
    template_name = 'portal_delete.html'

