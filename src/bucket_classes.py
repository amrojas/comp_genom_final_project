"""
Description: Contains the basic implementation for a Bucket in Cuckoo Filter

"""

class Bucket:

    def __init__(self, entries):
        self.size = entries
        self.bucket = []
    
    def isFull(self):
        if len(self.bucket) >= self.size:
            return True
        return False

    
