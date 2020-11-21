"""
Description: Contains the unit tests for Cuckoo Filter class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import cuckoo_filter

def test_construction():
    """ Ensures the cuckoo filter is constructed as we would expect """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8, 1, 500)
    assert cuckooFilter.num_buckets == 10
    assert cuckooFilter.fp_size == 8

def test_insert():
    """ Ensures the cuckoo filter can insert items we should be able to """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8, 1, 500)
    assert cuckooFilter.insert("GCGTTT") == True
    assert cuckooFilter.insert("GCGTTT") == True

def test_contains():
    """ Ensures you can find inserted strings and not find strings not inserted"""
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8, 1, 500)
    cuckooFilter.insert("GCGTTT")
    assert cuckooFilter.contains("GCGTTT") == True
    assert cuckooFilter.contains("TTT") == False

def test_delete():
    """ Ensures you can delete strings present in filter and cannot delete those not in filter """
    cuckooFilter = cuckoo_filter.CuckooFilter(10, 8, 1, 500)
    cuckooFilter.insert("GCGTTT")
    assert cuckooFilter.delete("GCGTTT") == True
    assert cuckooFilter.delete("GCGTTT") == False

def test_construction_stash():
    """ Ensures the cuckoo filter with stash is constructed as we would expect """
    cuckooFilterStash = cuckoo_filter.CuckooFilterStash(10, 8, 1, 500, 64)
    assert cuckooFilterStash.num_buckets == 10
    assert cuckooFilterStash.fp_size == 8
    assert cuckooFilterStash.total_capacity == 74
    assert cuckooFilterStash.stash_size == 64


def test_construction_bit():
    test_cuckoo = cuckoo_filter.CuckooFilterBit(10, 4, 4, 500)
    assert test_cuckoo.max_iter == 500
    assert test_cuckoo.num_items_in_filter == 0
    assert test_cuckoo.total_capacity == 40

def test_bit_insert_contains_remove():
    test_cuckoo = cuckoo_filter.CuckooFilterBit(10, 4, 4, 500)
    assert test_cuckoo.insert("GCGTT") == True
    assert test_cuckoo.contains("GCGTT") == True 

    assert test_cuckoo.contains("GCGTTTTT") == False 
    assert test_cuckoo.delete("GCGTT") == True 
    assert test_cuckoo.contains("GCGTT") == False 

