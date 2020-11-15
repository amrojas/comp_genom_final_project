"""
Description: Contains the implementation for a Cuckoo Filter with and without Stash
"""
import bucket_classes
import hashlib
import sys
import random
import math

class CuckooFilter:

    def __init__(self, num_buckets, fp_size, bucket_size, max_iter):
        """
        Creates a standard Cuckoo Filter.

            num_buckets --> how many buckets will the Cuckoo Filter contain
            fp_size --> the size of the fingerprint in bits that will stored in buckets
            bucket_size --> how many fingerprints can be stored in each bucket
            max_iter --> maximum number of displacements before giving up on that item
        """
        self.num_buckets = num_buckets
        self.fp_size = fp_size
        self.bucket_size = bucket_size
        self.max_iter = max_iter
        self.filter = [bucket_classes.Bucket(self.bucket_size) for i in range(num_buckets)]
        self.num_items_in_filter = 0
        self.total_capacity = self.bucket_size * self.num_buckets

    @staticmethod
    def get_hash_value(item):
        hash_sha256 = hashlib.sha256(str(item).encode('utf-8'))
        hash_result = hash_sha256.digest()
        hash_result_int = int.from_bytes(hash_result, byteorder='big')
        return hash_result_int

    @staticmethod
    def get_fingerprint(item, fp_size):
        """
            Gets a fingerprint for item trying to be inserted by hashing
            and taking the fp.size least significant bits. Returns an integer.
        """

        #Create a bit mask of self.fp_size bits
        mask_bits_int = int(("1" * fp_size), 2)
        mask_bytes = mask_bits_int.to_bytes((mask_bits_int.bit_length() // 8) + 1, byteorder='big')

        #Get hash value for the item trying to be inserted
        hash_result_int = CuckooFilter.get_hash_value(item)

        #Get fingerprint with bitwise-AND
        fp = hash_result_int & mask_bits_int
        return fp

    def get_fp_and_index_positions(self, item):
        fingerprint = CuckooFilter.get_fingerprint(item, self.fp_size)

        hash_x = CuckooFilter.get_hash_value(item)
        hash_fp = CuckooFilter.get_hash_value(fingerprint)

        index_one = hash_x % self.num_buckets
        index_two = (index_one ^ hash_fp) % self.num_buckets

        return [fingerprint, index_one, index_two]

    def insert(self, item):
        """
            Attempts to insert a new value and return True when it does
            and False when it cannot and that means the filter is full.
        """

        fingerprint, index_one, index_two = self.get_fp_and_index_positions(item)

        #Try to insert into one of those two buckets
        if not self.filter[index_one].isFull():
            self.filter[index_one].insert(fingerprint)
            self.num_items_in_filter += 1
            return True
        elif not self.filter[index_two].isFull():
            self.filter[index_two].insert(fingerprint)
            self.num_items_in_filter += 1
            return True

        #Try to relocate some of the items in bucket
        index = random.choice([index_one, index_two])
        for n in range(0, self.max_iter):
            fingerprint = self.filter[index].swap_with_random_entry(fingerprint)

            hash_fp = CuckooFilter.get_hash_value(fingerprint)
            index = (index ^ hash_fp) % self.num_buckets

            if not self.filter[index].isFull():
                self.filter[index].insert(fingerprint)
                self.num_items_in_filter += 1
                return True

        #We have failed to insert, filter is full
        return False

    def contains(self, item):
        fingerprint, index_one, index_two = self.get_fp_and_index_positions(item)

        if self.filter[index_one].contains(fingerprint) or self.filter[index_two].contains(fingerprint):
            return True
        return False

    def delete(self, item):
        fingerprint, index_one, index_two = self.get_fp_and_index_positions(item)

        if self.filter[index_one].contains(fingerprint):
            self.num_items_in_filter -= 1
            return self.filter[index_one].remove(fingerprint)
        elif self.filter[index_two].contains(fingerprint):
            self.num_items_in_filter -= 1
            return self.filter[index_two].remove(fingerprint)
        return False
    
    def get_size(self):
        """
        Returns the total number of bytes occupied by the filter object
        """
        agg = 0
        for b in self.filter:
            agg += b.get_size()
        return(
            sys.getsizeof(self.num_buckets) +
            sys.getsizeof(self.fp_size) +
            sys.getsizeof(self.bucket_size) +
            sys.getsizeof(self.max_iter) +
            sys.getsizeof(self.filter) +
            sys.getsizeof(self.num_items_in_filter) +
            agg
        )
class CuckooFilterStash(CuckooFilter):

    def __init__(self, num_buckets, fp_size, bucket_size, max_iter, stash_size):
        """
        Creates a Cuckoo Filter with Stash. 
            
            stash_size --> size of the stash list
        """
        super().__init__(num_buckets, fp_size, bucket_size, max_iter)
        self.stash_size = stash_size
        self.stash = bucket_classes.Bucket(self.stash_size)
        self.total_capacity += self.stash_size
    
    def insert(self, item):
        insert_result = super().insert(item)
        # print(insert_result)
        if not insert_result and not self.stash.isFull():
            self.num_items_in_filter += 1
            return self.stash.insert(item)
        return insert_result
    
    def contains(self, item):
        fingerprint, index_one, index_two = super().get_fp_and_index_positions(item)
        return (super.contains(item) or self.stash.contains(fingerprint))
    
    def delete(self, item):
        delete_result = super().delete(item)
        fingerprint, index_one, index_two = super().get_fp_and_index_positions(item)
        if not delete_result and self.stash.contains(fingerprint):
            self.num_items_in_filter -= 1
            return self.stash.remove(fingerprint)
        return delete_result

    def get_size(self):
        """
        Returns the total number of bytes occupied by the filter object
        """
        agg = 0
        for b in self.filter:
            agg += b.get_size()
        return(
            sys.getsizeof(self.num_buckets) +
            sys.getsizeof(self.fp_size) +
            sys.getsizeof(self.bucket_size) +
            sys.getsizeof(self.max_iter) +
            sys.getsizeof(self.filter) +
            sys.getsizeof(self.num_items_in_filter) +
            sys.getsizeof(self.stash_size) +
            sys.getsizeof(self.stash) +
            sys.getsizeof(self.total_capacity) +
            agg
        )

class CuckooFilterAuto(CuckooFilter):

    def __init__(self, expected_num, fp_prob):
        """
        Creates a Cuckoo Filter with given false positive probability and expected 
        number of items to be inserted. Then, parameters of filter are calculated
        to fit that case.
        """
        bucket_size = self.get_bucket_size(fp_prob)
        fp_size = self.get_fingerprint_size(expected_num, fp_prob, bucket_size)
        num_buckets = self.get_num_of_buckets(expected_num, bucket_size)
        super().__init__(num_buckets, fp_size, bucket_size, max_iter=500)
        self.fp_prob = fp_prob

    def get_bucket_size(self, fp_prob):
        """
        Based on heuristics in paper (Fan et al, 2014)
        """
        if fp_prob > 0.002:
            return 4
        else:
            return 8
    
    def get_fingerprint_size(self, num_buckets, fp_prob, bucket_size):
        """
        Based on heuristics in paper (Fan et al, 2014)
        """
        fp_size = math.ceil(math.log((1/fp_prob), 2) + math.log(2*bucket_size, 2))
        return fp_size
    
    def get_num_of_buckets(self, expected_num, bucket_size):
        """
        Based on heuristics in paper (Fan et al, 2014)
        """
        total_capacity = 0
        if bucket_size == 4:
            total_capacity = math.ceil(expected_num/0.95)
        elif bucket_size == 8:
            total_capacity = math.ceil(expected_num/0.98)
        num_buckets = math.ceil(total_capacity/bucket_size)
        return num_buckets

    def get_size(self):
        """
        Returns the total number of bytes occupied by the filter object
        """
        agg = 0
        for b in self.filter:
            agg += b.get_size()
        return(
            sys.getsizeof(self.num_buckets) +
            sys.getsizeof(self.fp_size) +
            sys.getsizeof(self.bucket_size) +
            sys.getsizeof(self.max_iter) +
            sys.getsizeof(self.filter) +
            sys.getsizeof(self.num_items_in_filter) + 
            sys.getsizeof(self.fp_prob) + 
            agg
        )