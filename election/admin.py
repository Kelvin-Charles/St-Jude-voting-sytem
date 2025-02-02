from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from .models import User, Election, Position, Candidate, Vote
from .admin_customization import admin_site

@admin.register(User, site=admin_site)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Election, site=admin_site)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.admin_site.admin_view(self.admin_site.election_view), name='election_index'),
        ]
        return my_urls + urls

    def election_index(self, request):
        app_list = self.get_app_list(request)
        context = {
            'title': 'Election Administration',
            'subtitle': 'Manage elections, candidates, and votes',
            'total_elections': Election.objects.count(),
            'total_users': User.objects.count(),
            'total_votes': Vote.objects.count(),
            'active_elections': Election.objects.filter(is_active=True).count(),
            'app_list': app_list,
            **self.admin_site.each_context(request),
        }
        return TemplateResponse(request, "admin/election/index.html", context)

    class Media:
        css = {
            'all': ['css/admin/election.css']
        }
        js = ['js/admin/election.js']

@admin.register(Position, site=admin_site)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election')
    list_filter = ('election',)
    search_fields = ('title', 'election__title')

@admin.register(Candidate, site=admin_site)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'get_election')
    list_filter = ('position__election', 'position')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
    def get_election(self, obj):
        return obj.position.election
    get_election.short_description = 'Election'
    get_election.admin_order_field = 'position__election'

@admin.register(Vote, site=admin_site)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'position', 'timestamp')
    list_filter = ('position__election', 'position', 'timestamp')
    search_fields = ('voter__username', 'candidate__user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('voter', 'candidate', 'position', 'timestamp') 