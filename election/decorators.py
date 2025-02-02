from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Election, Vote, Position

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def prevent_double_voting(view_func):
    @wraps(view_func)
    def wrapper(request, election_id, *args, **kwargs):
        election = get_object_or_404(Election, pk=election_id)
        positions = Position.objects.filter(election=election)
        voted_positions = Vote.objects.filter(
            voter=request.user,
            election=election
        ).values_list('position_id', flat=True)
        
        if voted_positions.count() >= positions.count():
            messages.warning(request, "You have already voted in all positions for this election.")
            return redirect('election:election-list')
        return view_func(request, election_id, *args, **kwargs)
    return wrapper 