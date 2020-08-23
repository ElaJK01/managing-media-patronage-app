from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import FormView, CreateView, UpdateView
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

    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     category = form.cleaned_data['category']
    #     address = form.cleaned_data['address']
    #     email = form.cleaned_data['email']
    #     logo = form.cleaned_data['logotype']
    #     comments = form.cleaned_data['comments']
    #     new_portal = Portal.objects.create(name=name, category=category, address=address, email=email, logotype=logo, comments=comments)
    #     new_portal.save()
    #     return super().form_valid(form)


class AddPerson(CreateView):
    template_name = 'person_form.html'
    model = Person
    fields = '__all__'
    success_url = reverse_lazy("person_list")


class PortalUpdateView(UpdateView):
    model = Portal
    fields = '__all__'
    success_url = reverse_lazy('portal_list')
    template_name = 'portal_form.html'


class PortalDetailView(DetailView):
    model = Portal

