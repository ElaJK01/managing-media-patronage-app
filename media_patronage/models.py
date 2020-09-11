from django.db import models
from phone_field import PhoneField


class Portal(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nazwa')
    category = models.CharField(max_length=60, verbose_name='Kategoria', help_text='Tematyka portalu')
    address = models.CharField(max_length=250, verbose_name='Adres redakcji')
    email = models.EmailField()
    logotype = models.ImageField(upload_to='logo/', verbose_name='Logo', null=True, blank=True)
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
    pdf_article = models.FileField(upload_to='articles/', null=True, verbose_name='PDF')

    def __str__(self):
        return {self.title}


class TaskBeforeEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, verbose_name='Wydarzenie')
    send_invitation_to_portals = models.BooleanField(default=False, verbose_name='czy wysłane zaproszenie do portali tematynych')
    when_send_invitation = models.DateField(verbose_name='Kiedy zostało wysłane zaproszenie', null=True, blank=True)
    portals_invited = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Zaproszone do współpracy portale')
    comments = models.TextField(verbose_name='Dodatkowe informacje', blank=True)

    # def __str__(self):
    #     return {self.pk}


class TaskAfterEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Wydarzenie')
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Portal', null=True)
    send_materials_after_event = models.BooleanField(default=False, verbose_name='Wysłane materiały pokonferencyjne')
    date_when_send = models.DateField(verbose_name='Data', null=True)
    comments = models.TextField(verbose_name='Dodatkowe informacje', blank=True)

    # def __str__(self):
    #     return self.pk

class CooperationTerms(models.Model):
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    services_for_portal = models.TextField()
    services_provided_by_portal = models.TextField()
    comments = models.TextField()


class Email(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    to_who = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='addressee')
    send_from_email = models.EmailField()




