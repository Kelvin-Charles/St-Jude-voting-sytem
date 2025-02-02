from django import template

register = template.Library()

@register.filter(name='filter_by_election')
def filter_by_election(votes, election):
    # Filter votes for a specific election
    return votes.filter(election=election)

@register.filter(name='can_vote')
def can_vote(election, user):
    # Return false if user is not logged in or election is not ongoing
    if not user or not election.is_ongoing():
        return False
        
    # Get positions for this election
    positions = election.positions.all()
    if not positions.exists():
        return False
        
    # Get positions user has already voted for
    voted_positions = election.vote_set.filter(
        voter=user
    ).values_list('position_id', flat=True)
    
    # Allow voting if user hasn't voted for all positions
    return voted_positions.count() < positions.count() 