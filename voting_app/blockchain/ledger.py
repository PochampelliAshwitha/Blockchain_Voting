import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_votes = []
        self.create_block(previous_hash='1')  # Genesis block

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.pending_votes,
            'previous_hash': previous_hash,
        }
        block['hash'] = self.hash(block)
        self.pending_votes = []
        self.chain.append(block)
        return block

    def add_vote(self, voter_id, candidate_name):
        vote = {
            'voter_id': voter_id,
            'candidate': candidate_name
        }
        self.pending_votes.append(vote)

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def get_chain(self):
        return self.chain
