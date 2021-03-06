from django.db import models
from phone_field import PhoneField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Portal(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nazwa')
    category = models.CharField(max_length=60, verbose_name='Kategoria', help_text='Tematyka portalu')
    address = models.CharField(max_length=250, verbose_name='Adres redakcji')
    email = models.EmailField()
    logotype = CloudinaryField('logotype', null=True, blank=True)
    comments = models.TextField(verbose_name='Inne informacje', blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f"/portal_details/{self.pk}/"


class Person(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Imię')
    last_name = models.CharField(max_length=20, verbose_name='Nazwisko')
    email = models.EmailField()
    phone_number = PhoneField()
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Portal')
    comments = models.TextField(verbose_name='Komentarz', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.portal}"

    def get_absolute_url(self):
        return f"/person_details/{self.pk}/"


class Event(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tytuł')
    date = models.DateField(verbose_name='Data')
    portals_cooperating = models.ManyToManyField(Portal, verbose_name='Portale współpracujące')

    def __str__(self):
        return f'{self.title} - {self.date}'

    def get_absolute_url(self):
        return f"/event_details/{self.pk}/"


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tytuł')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Wydarzenie', help_text='Wydarzenie, którego dotyczy')
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Na jakim portalu opublikowane')
    published_date = models.DateField(verbose_name='Data publikacji')
    pdf_article = CloudinaryField('pdf', null=True, format="jpg",)

    def __str__(self):
        return f'{self.title}'


class TaskBeforeEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Wydarzenie')
    comments = models.TextField(verbose_name='Dodatkowe informacje', blank=False)

    def __str__(self):
        return f'{self.comments}'


class TaskAfterEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Wydarzenie')
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Portal', null=True)
    send_materials_after_event = models.BooleanField(default=False, verbose_name='Wysłane materiały pokonferencyjne')
    date_when_send = models.DateField(verbose_name='Data', null=True)
    comments = models.TextField(verbose_name='Dodatkowe informacje', blank=True)


class CooperationTerms(models.Model):
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    services_for_portal = models.TextField(verbose_name='Usługi swiadczone dla poortalu')
    services_provided_by_portal = models.TextField(verbose_name='Usługi świadczone przez portal')
    comments = models.TextField(verbose_name='Uwagi', blank=True)
    date_update = models.DateField(verbose_name='Data dodania warunków wspólpracy', default=timezone.now())


class Email(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    to_who = models.ManyToManyField(Person, related_name='person_address')
    who_send = models.EmailField()
    date = models.DateField()

    def __str__(self):
        return f'{self.event} - {self.to_who}'




