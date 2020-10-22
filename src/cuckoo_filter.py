"""
Description: Contains the basic implementation for a Cuckoo Filter

"""

class CuckooFilter:

    def __init__(self, num_buckets, fp_size, bucket_size = 4, max_iter = 500):
        self.num_buckets = num_buckets
        self.fp_size = fp_size
        self.bucket_size = bucket_size
        self.max_iter = max_iter

    def getSize(self):
        return self.size
