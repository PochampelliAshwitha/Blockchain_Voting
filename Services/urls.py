from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from Services import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('vote/', views.vote, name='vote'),
    path("dash_voter/",views.dash_voter,name="dash_voter"),
    path("dash_candidate/",views.dash_candidate,name="dash_candidate"),
    path("dash_election_commission/",views.dash_election_commission,name="dash_election_commission"),
    path("set_vote_date/",views.set_vote_date,name="set_vote_date"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
