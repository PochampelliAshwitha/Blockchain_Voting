from django.shortcuts import render
from .models import VoteBlock
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate, Voter
from .blockchain import add_vote_block, create_genesis_block
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import ElectionPeriod, Candidate,VoteBlock

def dash_voter(request):
    candidates = Candidate.objects.select_related('user').all()
    return render(request,"voter_dashboard.html", {'candidates': candidates}) 

def dash_candidate(request):
    return render(request,"candidate_dashboard.html")


@csrf_exempt
@login_required
def vote(request):
    now = timezone.now()
    try:
        election_period = ElectionPeriod.objects.latest('start_time')  # You can filter for active if needed
    except ElectionPeriod.DoesNotExist:
        messages.error(request, "No active election period.")
        return redirect("dash_voter")

    if now < election_period.start_time or now > election_period.end_time:
        messages.error(request, "Voting is not active right now.")
        return redirect("dash_voter")

    try:
        voter = request.user.voter_profile
    except Voter.DoesNotExist:
        messages.error(request, "You are not registered as a voter.")
        return redirect("dash_voter")

    if voter.has_voted:
        voted_candidate = VoteBlock.objects.filter(voter=voter).last().candidate
        messages.warning(request, "You have already voted.")
        candidates = Candidate.objects.all()
        return render(request, "voting_page.html", {
            "candidates": candidates,
            "already_voted": True,
            "voted_candidate_id": voted_candidate.candidate_id
        })

    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")
        try:
            candidate = Candidate.objects.get(candidate_id=candidate_id)
        except Candidate.DoesNotExist:
            messages.error(request, "Invalid candidate.")
            return redirect("vote")

        add_vote_block(voter, candidate)
        voter.has_voted = True
        voter.save()

        messages.success(request, f"You have successfully voted for {candidate.user.username}.")
        return redirect("vote")

    candidates = Candidate.objects.all()
    return render(request, "voting_page.html", {"candidates": candidates})


from django.utils import timezone
from .models import ElectionPeriod

def dash_election_commission(request):
    vote_data = (
        VoteBlock.objects
        .filter(candidate__isnull=False)
        .values("candidate__user__username")
        .annotate(vote_count=Count("id"))
        .order_by("-vote_count")
    )

    labels = [item["candidate__user__username"] for item in vote_data]
    data = [item["vote_count"] for item in vote_data]

    total_votes = VoteBlock.objects.filter(candidate__isnull=False).count()
    total_voters = Voter.objects.count()
    total_candidates = Candidate.objects.count()

    # Get the latest election period or create one
    try:
        election_period = ElectionPeriod.objects.latest("start_time")
    except ElectionPeriod.DoesNotExist:
        election_period = ElectionPeriod.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1)
        )

    # Handle manual update
    if request.method == "POST":
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")
        if start and end:
            election_period.start_time = start
            election_period.end_time = end
            election_period.save()
            messages.success(request, "Voting period updated.")
            return redirect("dash_election_commission")

    context = {
        "labels": labels,
        "data": data,
        "total_voters": total_voters,
        "total_candidates": total_candidates,
        "total_votes": total_votes,
        "election_period": election_period,
    }

    return render(request, "election_commission_dashboard.html", context)

def set_vote_date(request):
    if request.method == "POST":
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        if start_time and end_time:
            election_period = ElectionPeriod.objects.create(
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, "Election period set successfully.")
            return redirect("set_vote_date")
        else:
            messages.error(request, "Please provide both start and end time.")

    return render(request, "set_vote_date.html")