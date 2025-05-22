from django.conf import settings
from django.contrib import admin
from django.urls import path
from Accounts import views
from django.conf.urls.static import static

urlpatterns = [
    path('voter/',views.voter,name="voter"),
    path('candidate/',views.candidate,name="candidate"),
    path('election_commission/',views.election_commission,name="election_commission"),
    path('validate/', views.validate, name='validate'),
    path('candidate_profile/', views.candidate_profile, name='candidate_profile'),
    path('voter_profile/', views.voter_profile, name='voter_profile'),

    path('logout',views.logout,name="logout"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
