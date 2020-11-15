"""
Description: Contains the unit tests for Bloom Filter class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import bloom_filter

def test_construction():
    """ Ensures the bloom filter is constructed as we would expect """
    bloomFilter = bloom_filter.BloomFilter(100000, 0.03)
    assert bloomFilter.expected_num == 100000
    assert bloomFilter.size == 729844
    assert bloomFilter.num_hashes == 5

def test_insert():
    """ Ensures the bloom filter can insert items and report they are in there """
    bloomFilter = bloom_filter.BloomFilter(100000, 0.03)
    assert bloomFilter.insert("GCGTTT") == True
    assert bloomFilter.contains("GCGTTT") == True

def test_contains():
    """ Ensures the bloom filter returns True/False when approriate with contains operations """
    bloomFilter = bloom_filter.BloomFilter(100000, 0.03)
    assert bloomFilter.insert("GCGTTT") == True
    assert bloomFilter.insert("AAACTG") == True
    assert bloomFilter.contains("GT") == False
    assert bloomFilter.contains("GTATCGGGT") == False
    assert bloomFilter.contains("GCGTTT") == True
    assert bloomFilter.contains("AAACTG") == True