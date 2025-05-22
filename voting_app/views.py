# voting_app/views.py

from django.shortcuts import render, redirect
from .forms import VoteForm
from .blockchain.ledger import Blockchain

# Initialize blockchain once (in memory)
blockchain = Blockchain()

def vote_page(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            voter_id = form.cleaned_data['voter_id']
            candidate = form.cleaned_data['candidate']

            # Add the vote to blockchain
            blockchain.add_vote(voter_id=voter_id, candidate_name=candidate)

            # Create a new block (optional, after every vote or every few votes)
            blockchain.create_block(previous_hash=blockchain.last_block()['hash'])

            return render(request, 'voting_app/success.html', {'voter_id': voter_id})
    else:
        form = VoteForm()

    return render(request, 'voting_app/vote.html', {'form': form})



def blockchain_page(request):
    chain = blockchain.get_chain()
    return render(request, 'voting_app/blockchain.html', {'chain': chain})


def admin_dashboard(request):
    chain = blockchain.get_chain()
    total_votes = sum(len(block['votes']) for block in chain)
    return render(request, 'voting_app/admin_dashboard.html', {
        'total_votes': total_votes,
        'blocks': len(chain),
    })


import matplotlib.pyplot as plt
import io
import urllib, base64

def graph_page(request):
    candidates = {}
    for block in blockchain.get_chain():
        for vote in block['votes']:
            candidate = vote['candidate']
            candidates[candidate] = candidates.get(candidate, 0) + 1

    # Plot
    fig, ax = plt.subplots()
    ax.bar(candidates.keys(), candidates.values())
    ax.set_xlabel('Candidates')
    ax.set_ylabel('Votes')
    ax.set_title('Voting Results')

    # Save graph into memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return render(request, 'voting_app/graph.html', {'graph': graph})
