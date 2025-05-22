from django.db import models
from Accounts.models import Candidate, Voter

class VoteBlock(models.Model):
    index = models.IntegerField()
    timestamp = models.FloatField()
    voter = models.ForeignKey(Voter, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def calculate_hash(self):
        import hashlib
        record = str(self.index) + str(self.timestamp) + str(self.voter_id_or_none()) + str(self.candidate_id_or_none()) + self.previous_hash
        return hashlib.sha256(record.encode()).hexdigest()

    def voter_id_or_none(self):
        return self.voter.voter_id if self.voter else "None"

    def candidate_id_or_none(self):
        return self.candidate.candidate_id if self.candidate else "None"


class ElectionPeriod(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Election Period: {self.start_time} to {self.end_time}"
