"""
Description: Contains the basic implementation for a Bucket in Cuckoo Filter
"""
import random
import sys
from sys import getsizeof
from bitarray import bitarray

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


class bitBucketArray:

    def __init__(self, buckets, num_entries, fp_size):
        """
        Creates a bucket array implemented with bitarrays.

            buckets --> how many buckets are in this array
            num_entries --> number of fingerprints in each bucket
            fp_size --> size in bits of fingerprints
        """
        self.num_buckets = buckets
        self.fp_size = fp_size
        self.num_entries = num_entries
        self.curr_entries_per_bucket = [0 for i in range(self.num_buckets)]
        self.filter = bitarray(self.fp_size * self.num_buckets * self.num_entries)
        self.filter.setall(0)
    
    @staticmethod
    def get_binary_string(fp_size, fp):
        format_str = "{0:0" + str(fp_size) + "b}"
        return format_str.format(fp)
    
    def get_inner_bucket_position(self, bucket_num, fp):
        start_pos = bucket_num * self.fp_size * self.num_entries
        end_pos = (bucket_num * self.fp_size * self.num_entries) + (self.curr_entries_per_bucket[bucket_num] * self.fp_size)
        bit_str = ""
        entry_pos = 0
        for bit_pos in range(start_pos, end_pos):
            if self.filter[bit_pos]: #Put together the fingerprint
                bit_str += "1"
            else:
                bit_str += "0"
            
            if (bit_pos+1) % 4 == 0: #Check if fingerprint matches
                curr_fp = int(bit_str, 2)
                if curr_fp == fp:
                    return entry_pos
                entry_pos += 1
                bit_str = ""

    def isFull(self, bucket_num):
        if self.curr_entries_per_bucket[bucket_num] >= self.num_entries:
            return True
        return False
    
    def contains(self, bucket_num, fp):
        start_pos = bucket_num * self.fp_size * self.num_entries
        end_pos = (bucket_num * self.fp_size * self.num_entries) + (self.curr_entries_per_bucket[bucket_num] * self.fp_size)
        bit_str = ""
        for bit_pos in range(start_pos, end_pos):
            if self.filter[bit_pos]: #Put together the fingerprint
                bit_str += "1"
            else:
                bit_str += "0"
            
            if (bit_pos+1) % 4 == 0: #Check if fingerprint matches
                curr_fp = int(bit_str, 2)
                if curr_fp == fp:
                    return True
                bit_str = ""
        return False
    
    def insert(self, bucket_num, fp):
        if not self.isFull(bucket_num):

            #Don't allow duplicates in same bucket
            if self.contains(bucket_num, fp):
                return False

            binary_str = bitBucketArray.get_binary_string(self.fp_size, fp)
            
            start_pos = (bucket_num * self.fp_size * self.num_entries) + (self.curr_entries_per_bucket[bucket_num] * self.fp_size)
            end_pos = (bucket_num * self.fp_size * self.num_entries) + ((self.curr_entries_per_bucket[bucket_num]+1) * self.fp_size)

            for pos in range(start_pos, end_pos): #Place fp in that bucket
                if binary_str[pos - start_pos] == "1":
                    self.filter[pos] = True
                else:
                    self.filter[pos] = False
            
            self.curr_entries_per_bucket[bucket_num] += 1
            return True

        return False
    
    def remove(self, bucket_num, fp):

        if self.contains(bucket_num, fp):
            inner_bucket_pos = self.get_inner_bucket_position(bucket_num, fp)

            #Zero out that fingerprint in bucket
            start_pos = (bucket_num * self.fp_size * self.num_entries) + (inner_bucket_pos * self.fp_size)
            end_pos = (bucket_num * self.fp_size * self.num_entries) + ((inner_bucket_pos+1) * self.fp_size)

            for pos in range(start_pos, end_pos):
                self.filter[pos] = False
            
            #Shift entries down if not the last one
            if inner_bucket_pos < (self.curr_entries_per_bucket[bucket_num]-1):

                start_pos = (bucket_num * self.fp_size * self.num_entries) + ((inner_bucket_pos+1) * self.fp_size)
                end_pos = (bucket_num * self.fp_size * self.num_entries) + (self.curr_entries_per_bucket[bucket_num] * self.fp_size)

                shift_str = ""
                for pos in range(start_pos, end_pos): #Get the fingerprints that will be shifted
                    if self.filter[pos]:
                        shift_str += "1"
                    else:
                        shift_str += "0"

                    self.filter[pos] = False
            
                #Now take shift_str and shift it down
                start_pos = (bucket_num * self.fp_size * self.num_entries) + (inner_bucket_pos * self.fp_size)
                end_pos = (bucket_num * self.fp_size * self.num_entries) + ((self.curr_entries_per_bucket[bucket_num]-1) * self.fp_size)

                for pos in range(start_pos, end_pos):
                    if shift_str[pos - start_pos] == "1":
                        self.filter[pos] = True
                    else:
                        self.filter[pos - start_pos] = False
            

            self.curr_entries_per_bucket[bucket_num] -= 1
            return True
        
        return False
    
    def get_bucket_list(self, bucket_num):
        
        start_pos = (bucket_num * self.fp_size * self.num_entries) 
        end_pos = (bucket_num * self.fp_size * self.num_entries) + (self.curr_entries_per_bucket[bucket_num] * self.fp_size)

        bucket_list = []

        bit_str = ""
        for pos in range(start_pos, end_pos):
            if self.filter[pos]: #Put together the fingerprint
                bit_str += "1"
            else:
                bit_str += "0"
            
            if (pos+1) % 4 == 0: #Check if fingerprint matches
                bucket_list.append(bit_str)
                bit_str = ""
        
        return bucket_list

    def swap_with_random_entry(self, bucket_num, fp_to_insert):

        bucket_list = self.get_bucket_list(bucket_num)
        chosen_fp_str = random.choice(bucket_list)
        chosen_fp_int = int(chosen_fp_str, 2)
        
        self.remove(bucket_num, chosen_fp_int)
        self.insert(bucket_num, fp_to_insert)
        
        return chosen_fp_int
    
    def get_size(self):
        return (sys.getsizeof(self.num_buckets) +
                sys.getsizeof(self.fp_size) + 
                sys.getsizeof(self.num_entries) +
                sys.getsizeof(self.curr_entries_per_bucket) +
                sys.getsizeof(self.filter))


    


    
