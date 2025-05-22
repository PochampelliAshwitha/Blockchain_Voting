from django.contrib import admin
from .models import Voter, Candidate

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'voter_id', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('created_at',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate_id', 'party', 'created_at')
    search_fields = ('user__username', 'party')
    list_filter = ('party', 'created_at')
