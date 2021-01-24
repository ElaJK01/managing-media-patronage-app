from django.contrib import admin
from .models import Portal, Person, Event, TaskAfterEvent, TaskBeforeEvent, Article, CooperationTerms, Email

# Register your models here.
admin.site.register(Portal)
admin.site.register(Person)
admin.site.register(Event)
admin.site.register(TaskAfterEvent)
admin.site.register(TaskBeforeEvent)
admin.site.register(Article)
admin.site.register(CooperationTerms)
admin.site.register(Email)