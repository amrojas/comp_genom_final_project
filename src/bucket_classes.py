"""
Description: Contains the basic implementation for a Bucket in Cuckoo Filter
"""
import random
import sys
from sys import getsizeof

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
        """ 
            Important point is that we do not allow duplicate items, which are allowed as
            described in Fan et. al (2014)
        """ 
        if not self.isFull() and fp not in self.bucket:
            self.bucket.append(fp)
            return True
        return False
    
    def remove(self, fp):
        if fp in self.bucket:
            self.bucket.remove(fp)
            return True
        return False
    
    def swap_with_random_entry(self, fp_to_insert):
        chosen_fp = random.choice(self.bucket)
        self.remove(chosen_fp)
        self.insert(fp_to_insert)
        return chosen_fp

    def get_size(self):
        return(sys.getsizeof(self.size) + sys.getsizeof(self.bucket))


    
