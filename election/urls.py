from django.urls import path
from . import views

app_name = 'election'

urlpatterns = [
    # Election views
    path('', views.ElectionListView.as_view(), name='election-list'),
    path('election/create/', views.create_election, name='election-create'),
    path('election/<int:election_id>/vote/', views.vote_view, name='vote'),
    path('election/<int:election_id>/results/', views.results_view, name='results'),
    
    # Position management
    path('election/<int:election_id>/position/add/', 
         views.position_create_view, name='position-create'),
    path('position/<int:position_id>/edit/', 
         views.position_edit_view, name='position-edit'),
    
    # Candidate management
    path('position/<int:position_id>/candidate/add/', 
         views.candidate_create_view, name='candidate-create'),
    path('candidate/<int:candidate_id>/edit/', 
         views.candidate_edit_view, name='candidate-edit'),
] 