
from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote_page, name='vote_page'),
    path('blockchain/', views.blockchain_page, name='blockchain_page'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('graph/', views.graph_page, name='graph_page'),

]
