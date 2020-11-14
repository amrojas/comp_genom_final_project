"""
Description: Contains the implementation for a Bloom Filter
"""

import mmh3
import math
from bitarray import bitarray

class BloomFilter:

    def __init__(self, expected_num, fp_prob):
        """
        Creates a standard Bloom Filter.

            expected_num --> expected number of items to input into bloom filter
            fp_prob --> false positive probability
        """

        self.fp_prob = fp_prob
        self.expected_num = expected_num
        self.size = self.get_filter_size()
        self.num_hashes = self.get_num_hashes()
        self.filter = bitarray(self.size)
        self.filter.setall(0)
    
    def insert(self, item):
        """
        Insert the given item into the bloom filter
        """
        for i in range(0, self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.filter[index] = 1
        return True
    
    def contains(self, item):
        """
        Check if item probably is in filter (True), and if definitely not (False)
        """
        for i in range(0, self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.filter[index] == 0:
                return False
        return True

    def get_filter_size(self):
        """
        Determine size of Bloom filter based on the desired false positive
        rate and expected number of items to be added.
        """
        size = (-1 * self.expected_num * math.log(self.fp_prob))/(math.log(2)**2)
        return int(size)

    
    def get_num_hashes(self):
        """
        Determine how many hash functions we need to use based on the size
        of the Bloom filter and items to be added.
        """
        k = (self.size/self.expected_num) * math.log(2)
        return int(k)