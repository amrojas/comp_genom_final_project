"""
Description: Contains the unit tests for Cuckoo Filter class
Author(s):
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import cuckoo_filter

def test_construction():
    """ Ensures the cuckoo filter is constructed as we would expect """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8)
    assert cuckooFilter.num_buckets == 10
    assert cuckooFilter.fp_size == 8

def test_insert():
    """ Ensures the cuckoo filter can insert items we should be able to """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8, 1)
    assert cuckooFilter.insert("GCGTTT") == True
    assert cuckooFilter.insert("GCGTTT") == True

def test_contains():
    """ Ensures you can find inserted strings and not find strings not inserted"""
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8)
    cuckooFilter.insert("GCGTTT")
    assert cuckooFilter.contains("GCGTTT") == True
    assert cuckooFilter.contains("TTT") == False

def test_delete():
    """ Ensures you can delete strings present in filter and cannot delete those not in filter """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8)
    cuckooFilter.insert("GCGTTT")
    assert cuckooFilter.delete("GCGTTT") == True
    assert cuckooFilter.delete("GCGTTT") == False