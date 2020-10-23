"""
Description: Contains the basic implementation for a Cuckoo Filter
"""
import bucket_classes
import hashlib
import sys

class CuckooFilter:

    def __init__(self, num_buckets, fp_size, bucket_size = 4, max_iter = 500):
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
            return True
        elif not self.filter[index_two].isFull():
            self.filter[index_two].insert(fingerprint)
            return True

        #Try to relocate some of the items in bucket
        index = random.choice([index_one])
        for n in range(0, self.max_iter):
            fingerprint = self.filter[index].swap_with_random_entry(fingerprint)

            hash_fp = CuckooFilter.get_hash_value(fingerprint)
            index = (index ^ hash_fp) % self.num_buckets

            if not self.filter[index].isFull():
                self.filter[index].insert(fingerprint)
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
            return self.filter[index_one].remove(fingerprint)    
        elif self.filter[index_two].contains(fingerprint):
            return self.filter[index_two].remove(fingerprint)        
        return False





