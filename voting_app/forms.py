# voting_app/forms.py

from django import forms

CANDIDATE_CHOICES = [
    ('Alice', 'Alice'),
    ('Bob', 'Bob'),
    ('Charlie', 'Charlie'),
]

class VoteForm(forms.Form):
    voter_id = forms.CharField(label='Your Voter ID', max_length=100)
    candidate = forms.ChoiceField(choices=CANDIDATE_CHOICES, widget=forms.RadioSelect)
