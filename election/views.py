from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

from .models import Election, Position, Candidate, Vote, User
from .forms import ElectionForm, PositionForm, CandidateForm, VoteForm, StudentRegistrationForm
from .decorators import admin_required, prevent_double_voting
from .utils import send_election_notifications, send_vote_confirmation

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class ElectionListView(LoginRequiredMixin, ListView):
    model = Election
    template_name = 'election/election_list.html'
    context_object_name = 'elections'

    def get_queryset(self):
        if self.request.user.is_admin():
            return Election.objects.all()
        return Election.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )

class ElectionDetailView(LoginRequiredMixin, DetailView):
    model = Election
    template_name = 'election/election_detail.html'
    context_object_name = 'election'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = self.object.positions.all()
        return context

@admin_required
def create_election(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            
            # Send notifications to all eligible voters
            eligible_voters = User.objects.filter(role='student', is_active=True)
            if send_election_notifications(request, election, eligible_voters):
                messages.success(request, 'Election created and notifications sent successfully.')
            else:
                messages.warning(request, 'Election created but there was an error sending notifications.')
            
            return redirect('election:election-detail', pk=election.pk)
    else:
        form = ElectionForm()
    
    return render(request, 'election/election_form.html', {'form': form})

@admin_required
def edit_election(request, pk):
    election = get_object_or_404(Election, pk=pk)
    
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, 'Election updated successfully.')
            return redirect('election:election-detail', pk=election.pk)
    else:
        form = ElectionForm(instance=election)
    
    return render(request, 'election/election_form.html', {
        'form': form,
        'election': election
    })

@login_required
@prevent_double_voting
def vote_view(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if not election.is_ongoing():
        messages.error(request, "This election is not currently active.")
        return redirect('election:election-list')
    
    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    for field_name, candidate in form.cleaned_data.items():
                        if field_name.startswith('position_'):
                            Vote.objects.create(
                                voter=request.user,
                                candidate=candidate,
                                election=election,
                                position=candidate.position
                            )
                    if send_vote_confirmation(request, request.user, election):
                        messages.success(request, "Your vote has been recorded successfully!")
                    else:
                        messages.warning(request, "Your vote was recorded but there was an error sending the confirmation email.")
                    return redirect('election:election-list')
            except Exception as e:
                messages.error(request, "An error occurred while recording your vote.")
    else:
        form = VoteForm(election)
    
    return render(request, 'election/vote_form.html', {
        'form': form,
        'election': election
    })

@login_required
def results_view(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if election.is_ongoing() and not request.user.is_admin():
        messages.error(request, "Results will be available after the election ends.")
        return redirect('election:election-list')
    
    results = election.get_results()
    return render(request, 'election/results.html', {
        'election': election,
        'results': results
    })

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('election:election-list')

class CustomLogoutView(LogoutView):
    next_page = 'login'

def register_view(request):
    if request.user.is_authenticated:
        return redirect('election:election-list')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the voting system.')
            return redirect('election:election-list')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@admin_required
def position_create_view(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.election = election
            position.save()
            messages.success(request, 'Position added successfully.')
            return redirect('election:election-detail', pk=election.pk)
    else:
        form = PositionForm()
    
    return render(request, 'election/position_form.html', {
        'form': form,
        'election': election
    })

@admin_required
def position_edit_view(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position updated successfully.')
            return redirect('election:election-detail', pk=position.election.pk)
    else:
        form = PositionForm(instance=position)
    
    return render(request, 'election/position_form.html', {
        'form': form,
        'position': position,
        'election': position.election
    })

@admin_required
def candidate_create_view(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.position = position
            candidate.save()
            messages.success(request, 'Candidate added successfully.')
            return redirect('election:position-detail', pk=position.pk)
    else:
        form = CandidateForm()
    
    return render(request, 'election/candidate_form.html', {
        'form': form,
        'position': position
    })

@admin_required
def candidate_edit_view(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated successfully.')
            return redirect('election:position-detail', pk=candidate.position.pk)
    else:
        form = CandidateForm(instance=candidate)
    
    return render(request, 'election/candidate_form.html', {
        'form': form,
        'candidate': candidate,
        'position': candidate.position
    }) 