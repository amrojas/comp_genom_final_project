"""
Description: Contains the basic implementation for a Bucket in Cuckoo Filter
"""

class Bucket:

    def __init__(self, entries):
        """
        Creates a standard bucket.

            size --> how many fingerpritns will this bucket store
            bucket --> python list that stores fingerprints
        """
        self.size = entries
        self.bucket = []
    
    def isFull(self):
        if len(self.bucket) >= self.size:
            return True
        return False
    
    def contains(self, fp):
        return (fp in self.bucket)
    
    def insert(self, fp):
        """ Important point is that duplicate items are allowed as
            described in Fan et. al (2014)
        """ 
        if not self.isFull():
            self.bucket.append(fp)
            return True
        return False
    
    def remove(self, fp):
        if fp in self.bucket:
            self.bucket.remove(fp)
            return True
        return False

    
