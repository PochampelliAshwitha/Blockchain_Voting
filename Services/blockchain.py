# blockchain.py

from .models import VoteBlock, Voter, Candidate
import time

def get_last_block():
    return VoteBlock.objects.order_by('-index').first()

def create_genesis_block():
    if VoteBlock.objects.count() == 0:
        genesis_block = VoteBlock(
            index=0,
            timestamp=time.time(),
            voter=None,
            candidate=None,
            previous_hash='0'
        )
        genesis_block.hash = genesis_block.calculate_hash()
        genesis_block.save()

def is_chain_valid():
    blocks = VoteBlock.objects.order_by('index')
    for i in range(1, blocks.count()):
        current_block = blocks[i]
        previous_block = blocks[i-1]
        if current_block.previous_hash != previous_block.hash:
            return False
        if current_block.hash != current_block.calculate_hash():
            return False
    return True

def add_vote_block(voter: Voter, candidate: Candidate):
    last_block = get_last_block()
    index = last_block.index + 1 if last_block else 1
    previous_hash = last_block.hash if last_block else '0'
    new_block = VoteBlock(
        index=index,
        timestamp=time.time(),
        voter=voter,
        candidate=candidate,
        previous_hash=previous_hash
    )
    new_block.hash = new_block.calculate_hash()
    new_block.save()
