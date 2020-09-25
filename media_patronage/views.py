from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .forms import AddEventForm, AddPortalForm, AddPersonForm, SearchForm, TaskAfterForm, TaskBeforeForm
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms, Email
from django.db.models import Q
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
from .render import Render
from django.utils import timezone
from django.core.paginator import Paginator

class EventList(ListView):
    paginate_by = 20
    model = Event
    ordering = ['date']


class AddEvent(FormView):
    template_name = "event_form.html"
    form_class = AddEventForm
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EventDetailsView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        tasks_after = TaskAfterEvent.objects.filter(event=event)
        tasks_before = TaskBeforeEvent.objects.filter(event=event)
        cooperation_terms = CooperationTerms.objects.filter(event=event)
        context = { 'event': event,
                    'tasks_after': tasks_after,
                    'tasks_before': tasks_before,
                     'cooperation_terms': cooperation_terms}
        return render(request, 'event_detail.html', context)


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')
    template_name = 'event_delete.html'


class EventAddPortalView(View):
    def get(self, request, pk):
        event_to_update = Event.objects.get(pk=pk)
        if event_to_update:
            ctx = {'event': event_to_update}
            return render(request, 'event_add_portal.html', ctx)
        else:
            msg = {'msg': 'Nie ma takiego wydarzenia!'}
            return render(request, 'event_add_portal.html', msg)

    def post(self, request, pk):
        event_to_update = Event.objects.get(pk=pk)
        portal= request.POST.get('portal')
        portal_to_add = Portal.objects.get(name=portal)
        event_to_update.portals_cooperating.add(portal_to_add)
        event_to_update.save()
        return redirect(f'/event_details/{event_to_update.pk}')


class EventUpdateView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        ctx = {'event': event}
        return render(request, 'event_update.html', ctx)

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        date_updated = request.POST.get('date')
        title_updated = request.POST.get('title')
        event.date = date_updated
        event.title = title_updated
        event.save()
        return redirect(f'event_details/{event.pk}')


class EventRemovePortalView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        ctx = {'event': event}
        return render(request, "event_remove_portal.html", ctx)

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        portal_to_remove_name = request.POST.get('portal_to_remove')
        portal_to_remove = Portal.objects.get(name=portal_to_remove_name)
        task_after = TaskAfterEvent.objects.get(event=event)
        event.portals_cooperating.remove(portal_to_remove)
        event.save()
        task_after.delete()
        return redirect(f'/event_details/{event.pk}')


class PortalList(ListView):
    paginate_by = 10
    model = Portal
    ordering = ['name']



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
                events = Event.objects.filter(Q(title__icontains = search_que) | Q(date__icontains = search_que))
                result_portal = [portal for portal in portals]
                result_person = [person for person in persons]
                result_event = [event for event in events]
                result = result_portal+result_person+result_event
            else:
                result = []
        else:
            form = SearchForm()
            result = None
        ctx = {"result": result,
               "form": form}
        return ctx


class PersonList(ListView):
    paginate_by = 20
    model = Person
    ordering = ['last_name']


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


class TaskAfterEventView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        if event:
            event_portals = event.portals_cooperating.all()
            ctx = {'event': event,
               'event_portals': event_portals}
            return render(request, 'tasks_after.html', ctx)
        else:
            return HttpResponse("Nie ma takiego wydarzenia!")

    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        event_portal_name = request.POST.get('portal')
        event_portal = Portal.objects.get(name=event_portal_name)
        send_materials_after = "send" in request.POST
        when_send_materials = request.POST.get('date')
        comments = request.POST.get('comments')
        if event and event_portal and send_materials_after and when_send_materials:
            task = TaskAfterEvent.objects.create(event=event, portal = event_portal, send_materials_after_event=send_materials_after,
                                          date_when_send=when_send_materials, comments=comments)
            task.save()
            return redirect('event_list')
        else:
            return HttpResponse('Błędnie wypełniony formularz!')


class TaskBeforeEventView(CreateView):
    template_name = 'tasks_before.html'
    form_class = TaskBeforeForm
    success_url = reverse_lazy("event_list")

#FIXME wybór portali do wysyłki, zwalidować datę wysłania zaproszeń nie może być po terminie konferencji
    # def get(self, request, pk):
    #     event = get_object_or_404(Event, pk=pk)
    #     form = TaskBeforeForm()
    #     ctx = {'form': form,
    #            'event': event}
    #     return render(request, 'tasks_before.html', ctx)
    #
    # def post(self, request, pk):
    #     event = Event.objects.get(pk=pk)
    #     send_invitation_to_portals = request.POST.get('send_invitation')
    #     when_send_invitation = request.POST.get('when_send_invitation')
    #     event_date = str(event.date)
    #     portals_invited = request.POST.get('portals_invited')
    #     comments = request.POST.get('comments')
    #     if when_send_invitation < event_date:
    #         msg = {'msg': 'Podana data wysłania jest niewłaściwa'}
    #         return render(request, 'tasks_before.html', msg)
    #     else:
    #         task_before = TaskBeforeEvent.objects.create(event=event, send_invitation_to_portals=send_invitation_to_portals,
    #                                                      when_send_invitation=when_send_invitation, portals_invited=portals_invited,
    #                                                      comments=comments)
    #         task_before.save()
    #         return redirect('event_detail')

class PdfView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        today = timezone.now()
        tasks_after = TaskAfterEvent.objects.filter(event=event)
        tasks_before = TaskBeforeEvent.objects.filter(event=event)
        cooperation_terms = CooperationTerms.objects.filter(event=event)
        params = {'event': event,
                   'tasks_after': tasks_after,
                   'tasks_before': tasks_before,
                   'cooperation_terms': cooperation_terms,
                  'today': today}

        return Render.render('pdf.html', params)


class ArticleAddView(CreateView):
    model = Article
    template_name = 'article_form.html'
    fields = '__all__'
    success_url = reverse_lazy('article_list')


class ArticleList(ListView):
    paginate_by = 20
    model = Article
    ordering = ['title']


class AddCooperationTerms(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event:
            ctx = {'event':event,
                 }
            return render(request, "add_cooperation_terms.html", ctx)

    def post(self, request, pk):
        event=get_object_or_404(Event, pk=pk)
        portal_name = request.POST.get('portal')
        portal= Portal.objects.get(name=portal_name)
        services_for_p = request.POST.get('services_for_p')
        services_by_p = request.POST.get('services_by_p')
        comments = request.POST.get('comments')
        if event and portal and services_for_p and services_by_p:
            terms = CooperationTerms.objects.create(event=event, portal=portal, services_for_portal=services_for_p,
                                            services_provided_by_portal=services_by_p, comments=comments)
            terms.save()
            return redirect(f'/event_details/{event.pk}')
        else:
            ctx = {'msg': 'Niepoprawnie wykonany formularz!',
                   'event': event}
            return render(request, "add_cooperation_terms.html", ctx)


class MailingView(View):
    def get(self, request):
        return render(request, 'mailing.html')

    def post(self, request):
        event_it_concernse_title = request.POST.get('event')
        event_it_concernse =Event.objects.get(title=event_it_concernse_title)
        message_title = request.POST.get('message_title')
        who_send = request.POST.get('who_send')
        category = request.POST.getlist('category') #lista wybranych kategorii
        print(category)
        message = request.POST.get('message')
        if message_title and who_send and category:
            try:
                #wybranie z bazy portali należących do podanych kategorii
                portals_c = []
                for i in range(0, len(category)):
                    portals = Portal.objects.filter(category=category[i]) #otrzymujemy queryset portali do 1 z kategorii
                    i += 1
                    for p in portals: #iteruje po querysecie składającym się z portali jednej kategorii
                        portals_c.append(p) #dodajemy każdy portal do listy portali wskazanych przez użytkownika kategorii
                print(portals_c)
                persons =[] #pusta lista osób
                persons_addressee_emails = []  # pusta lista adresów email osób
                for portal in portals_c:#wybranie osób z każdego portalu
                    portal_persons = portal.person_set.all()
                    persons_list = [person for person in portal_persons]
                    persons = persons+persons_list

                print(persons)
                print(type(persons))
                for person in persons: #wybranie adresów email osób
                    persons_addressee_emails.append(person.email)
                print(persons_addressee_emails)

                email = Email.objects.create(event=event_it_concernse, message=message, send_from_email=who_send)
                persons=list(persons)
                email.to_who.set(persons)
                email.save()

                message1 = (message_title, message, who_send, persons_addressee_emails)
                send_mass_mail((message1,))
                msg = {'msg': f'Email został wysłany do:',
                       'emails': persons_addressee_emails}
                return render(request, 'mailing.html', msg)

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Upewnij się, że wszystkie pola są wypełnione!')











