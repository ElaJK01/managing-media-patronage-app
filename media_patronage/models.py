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
        return f"{self.first_name} {self.last_name}"


class Event(models.Model):
    title = models.CharField(max_length=250, verbose_name='Tytuł')
    date = models.DateField(verbose_name='Data')
    portals_cooperating = models.ManyToManyField(Portal)

    def __str__(self):
        return {self.title}


class Article(models.Model):
    title = models.CharField(max_length=250)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    published_date = models.DateField()
    pdf_article = models.FileField(upload_to='articles/', null=True)

    def __str__(self):
        return {self.title}


class TaskBeforeEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    send_invitation_to_portals = models.BooleanField(default=False)
    when_send_invitation = models.DateField()
    portals_invited = models.ForeignKey(Portal, on_delete=models.CASCADE)
    comments = models.TextField()


class TaskAfterEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    send_materials_after_event = models.BooleanField(default=False)
    date_when_send = models.DateField
    comments = models.TextField()


class CooperationTerms(models.Model):
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    services_for_portal = models.TextField()
    services_provided_by_portal = models.TextField()
    comments = models.TextField()




