from django.contrib import admin
from django.contrib import admin
from .models import ElectionPeriod
from .models import VoteBlock

@admin.register(VoteBlock)
class VoteBlockAdmin(admin.ModelAdmin):
    list_display = ('index', 'timestamp', 'voter', 'candidate', 'previous_hash', 'hash')
    search_fields = ('voter__voter_id', 'candidate__candidate_id')
    list_filter = ('voter', 'candidate')

@admin.register(ElectionPeriod)
class ElectionPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')
