"""portale_medialne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path

from media_patronage.views import EventList, AddEvent, PortalList, PersonList, AddPortal, AddPerson, SearchFormView,\
                            PortalUpdateView, PortalDetailView, PortalDeleteView, PersonDetailView, PersonUpdateView,\
                            PersonDeleteView, EventDetailsView, EventAddPortalView, EventRemovePortalView,\
                            EventDeleteView, TaskAfterEventView,TaskBeforeEventView, ArticleAddView, ArticleList, \
                            AddCooperationTerms, EventUpdateView, MailingView, PdfView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EventList.as_view(), name='event_list'),
    path('add_event/', AddEvent.as_view(), name='event_form'),
    path('portals/', PortalList.as_view(), name='portal_list'),
    path('persons/', PersonList.as_view(), name='person_list'),
    path('add_portal/', AddPortal.as_view(), name='portal_form'),
    path('add_person/', AddPerson.as_view(), name='person_form'),
    path('search/', SearchFormView.as_view(), name='search'),
    path('portal_details/<int:pk>/', PortalDetailView.as_view(), name='portal_detail'),
    path('portal_details/<int:pk>/update/', PortalUpdateView.as_view(), name='portal_update'),
    path('portal_details/<int:pk>/delete/', PortalDeleteView.as_view(), name='portal_delete'),
    path('person_details/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
    path('person_details/<int:pk>/update/', PersonUpdateView.as_view(), name='person_update'),
    path('person_details/<int:pk>/delete/', PersonDeleteView.as_view(), name='person_delete'),
    path('event_details/<int:pk>/', EventDetailsView.as_view(), name='event_detail'),
    path('event_details/<int:pk>/event_add_portal/', EventAddPortalView.as_view(), name='event_add_portal'),
    path('event_details/<int:pk>/event_remove_portal/', EventRemovePortalView.as_view(), name='event_remove_portal'),
    path('event_details/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('tasks_after/<int:pk>/', TaskAfterEventView.as_view(), name='tasks_after'),
    path('tasks_before/<int:pk>/', TaskBeforeEventView.as_view(), name='tasks_before'),
    path('add_article/', ArticleAddView.as_view(), name='article_form'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('add_terms/<int:pk>/', AddCooperationTerms.as_view(), name="add_terms"),
    path('event_details/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('mailing/', MailingView.as_view(), name='mailing'),
    path('render/pdf/<int:pk>/', PdfView.as_view(), name='pdf'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)