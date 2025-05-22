from django.db import models
from django.contrib.auth.models import User
import uuid

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter_profile')
    voter_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='voter_photos/')
    has_voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Voter ID: {self.voter_id}"

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    candidate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    party = models.CharField(max_length=100)
    manifesto = models.TextField()
    photo = models.ImageField(upload_to='candidate_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Candidate ID: {self.candidate_id}"
    
    