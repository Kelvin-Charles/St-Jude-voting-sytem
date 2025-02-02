from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Election, Position, Candidate, Vote

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'student_id', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'student_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'student_id', 'email', 'first_name', 'last_name'),
        }),
    )

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election', 'get_candidates_count')
    list_filter = ('election',)
    search_fields = ('title', 'description')

    def get_candidates_count(self, obj):
        return obj.candidates.count()
    get_candidates_count.short_description = 'Candidates'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'get_election')
    list_filter = ('position__election', 'position')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bio')

    def get_election(self, obj):
        return obj.position.election
    get_election.short_description = 'Election'
    get_election.admin_order_field = 'position__election'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'position', 'election', 'timestamp')
    list_filter = ('election', 'position', 'timestamp')
    search_fields = ('voter__username', 'candidate__user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',) 