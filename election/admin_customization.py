from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.db.models import Count
from django.utils import timezone
from election.models import User, Vote, Election, Position, Candidate

class ElectionAdminSite(AdminSite):
    site_header = "St Jude School Election Administration"
    site_title = "Election Admin"
    index_title = "Election Management"
    
    def index(self, request, extra_context=None):
        # Redirect admin index to election dashboard
        return redirect('admin:election_dashboard')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('election/', self.admin_view(self.election_view), name='election_view'),
            path('analytics/', self.admin_view(self.analytics_view), name='analytics'),
        ]
        return custom_urls + urls
    
    def login(self, request, extra_context=None):
        # Override login to redirect to dashboard after successful login
        response = super().login(request, extra_context)
        if request.method == 'POST' and request.user.is_authenticated:
            return redirect('admin:dashboard')
        return response

    def dashboard_view(self, request):
        # Get statistics
        total_users = User.objects.count()
        total_votes = Vote.objects.count()
        total_elections = Election.objects.count()
        active_elections = Election.objects.filter(is_active=True).count()
        
        # Get recent activities
        recent_votes = Vote.objects.select_related(
            'voter', 'candidate__user', 'position'
        ).order_by('-timestamp')[:5]
        
        recent_users = User.objects.order_by('-date_joined')[:5]
        
        # Get election statistics
        elections_by_votes = Election.objects.annotate(
            vote_count=Count('positions__vote')
        ).order_by('-vote_count')[:5]
        
        context = {
            **self.each_context(request),
            'title': 'Dashboard',
            'total_users': total_users,
            'total_votes': total_votes,
            'total_elections': total_elections,
            'active_elections': active_elections,
            'recent_votes': recent_votes,
            'recent_users': recent_users,
            'elections_by_votes': elections_by_votes,
        }
        return TemplateResponse(request, "admin/dashboard.html", context)
    
    def analytics_view(self, request):
        # Add analytics data
        monthly_votes = Vote.objects.extra(
            select={'month': 'EXTRACT(month FROM timestamp)'}
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        # Get election participation stats
        election_stats = Election.objects.annotate(
            total_votes=Count('positions__vote'),
            total_voters=Count('positions__vote__voter', distinct=True)
        )
        
        context = {
            **self.each_context(request),
            'title': 'Analytics',
            'monthly_votes': monthly_votes,
            'election_stats': election_stats,
        }
        return TemplateResponse(request, "admin/analytics.html", context)

    def election_view(self, request):
        context = {
            **self.each_context(request),
            'title': 'Election Administration',
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'recent_votes': Vote.objects.select_related('voter').order_by('-timestamp')[:5],
            'total_users': User.objects.count(),
            'total_votes': Vote.objects.count(),
            'total_elections': Election.objects.count(),
            'active_elections': Election.objects.filter(is_active=True).count(),
        }
        return TemplateResponse(request, "admin/election/index.html", context)

    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            'total_users': User.objects.count(),
            'total_votes': Vote.objects.count(),
            'total_elections': Election.objects.count(),
            'active_elections': Election.objects.filter(is_active=True).count(),
            'recent_activities': Vote.objects.select_related(
                'voter', 'candidate__user', 'position'
            ).order_by('-timestamp')[:10]
        })
        return context

# Create the custom admin site instance
admin_site = ElectionAdminSite(name='election_admin') 