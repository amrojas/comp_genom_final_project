"""
Description: Contains the unit tests for Bucket class

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import bucket_classes


def test_bucket_creation():
    """ Makes sure the bucket instance variables are as expected when created """
    num_entries = 4
    test_bucket = bucket_classes.Bucket(num_entries)
    assert test_bucket.size == num_entries
    assert test_bucket.bucket == []

def test_insert():
    """ Makes sure we insert correctly and we cannot insert at full bucket """
    num_entries = 2
    test_bucket = bucket_classes.Bucket(num_entries)
    test_bucket.insert(0b1111)
    assert test_bucket.contains(0b1111) == True
    assert test_bucket.insert(0b1111) == True
    assert test_bucket.insert(0b1011) == False

def test_bucket_full():
    """ Ensures that a bucket's isFull() works as expected """
    num_entries = 2
    test_bucket = bucket_classes.Bucket(num_entries)
    test_bucket.insert(0b0111) 
    test_bucket.insert(0b0001)
    assert test_bucket.isFull() == True
    
    test_bucket.remove(0b0001)
    assert test_bucket.isFull() == False

def test_contains():
    """ Ensures that contains works after insertions and removals, and uninserted items """
    num_entries = 2
    test_bucket = bucket_classes.Bucket(num_entries)
    test_bucket.insert(0b1111)
    assert test_bucket.contains(0b1111) == True
    assert test_bucket.contains(0b1110) == False
    test_bucket.remove(0b1111)
    assert test_bucket.contains(0b1111) == False

def test_remove():
    """ Ensures we can remove items in bucket and cannot for items not in bucket """
    num_entries = 2
    test_bucket = bucket_classes.Bucket(num_entries)    
    test_bucket.insert(0b0011)
    assert test_bucket.remove(0b0011) == True
    assert test_bucket.remove(0b0011) == False

def test_swap_random_entry():
    """ Ensure we can we can swap with a entry in bucket """
    num_entries = 2
    test_bucket = bucket_classes.Bucket(num_entries)    
    test_bucket.insert(0b0011)
    test_bucket.insert(0b0011)
    assert test_bucket.swap_with_random_entry(0b1100) == 0b0011
    

