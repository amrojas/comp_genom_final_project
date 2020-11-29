"""
Description: Contains the unit tests for CuckooBitTree class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from cuckoo_bit_tree import CuckooBitTree
from read import Read


def test_construction():
    """ Ensures the cuckoo Tree is constructed as we would expect """
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    assert cuckoo_tree.num_buckets == 10
    assert cuckoo_tree.fp_size == 8
    assert cuckoo_tree.root is None
    assert cuckoo_tree.theta == 0.5
    assert cuckoo_tree.k == 3


def test_single_read():
    """
    Ensures the cuckoo tree can
    1. create the new node and set is as root
    2. insert all 3-mers from read into the filter
    3. set the read_id of the leaf
    """
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    read_1 = Read('a.fastq', 'a', None, 'GCGT', 'IIII')
    cuckoo_tree.insert(read_1)
    assert cuckoo_tree.root is not None
    assert cuckoo_tree.root.parent is None
    assert cuckoo_tree.root.children == []
    assert cuckoo_tree.root.read_id == 'a'
    assert cuckoo_tree.root.filter.contains('GCG')
    assert cuckoo_tree.root.filter.contains('CGT')


def test_single_read_queries():
    """
    Ensures that we can query a single leaf/single node tree
    """
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    read_1 = Read('a.fastq', 'a', None, 'GCGT', 'IIII')
    cuckoo_tree.insert(read_1)
    assert cuckoo_tree.query('AAAA') == []
    assert cuckoo_tree.query('GCGT') == ['a']
    assert cuckoo_tree.query('ACGT') == ['a']
    assert cuckoo_tree.query('GCGA') == ['a']
    cuckoo_tree.theta = 0.6
    assert cuckoo_tree.query('AAAA') == []
    assert cuckoo_tree.query('GCGT') == ['a']
    assert cuckoo_tree.query('ACGT') == []
    assert cuckoo_tree.query('GCGA') == []


def test_create_internal_node():
    """
    Ensure that cuckoo tree can
    1. create an internal node
    2. set 2 reads as children of internal node
    2. put kmer info of both reads into internal node
    3. internal node has no read_id
    """
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    read_1 = Read('a.fastq', 'a', None, 'ABCD', 'IIII')
    read_2 = Read('b.fastq', 'b', None, 'EFGH', 'IIII')
    cuckoo_tree.insert(read_1)
    read_1_leaf = cuckoo_tree.root
    cuckoo_tree.insert(read_2)
    internal_node = cuckoo_tree.root
    idx = internal_node.children.index(read_1_leaf)
    read_2_leaf = internal_node.children[(idx + 1) % 2]
    assert internal_node.read_id is None
    assert internal_node.num_children() == 2
    assert internal_node.parent is None
    assert read_1_leaf in internal_node.children
    assert read_2_leaf in internal_node.children
    assert read_1_leaf.parent == internal_node
    assert read_2_leaf.parent == internal_node
    assert read_1_leaf.children == []
    assert read_2_leaf.children == []
    assert read_1_leaf.read_id == 'a'
    assert read_2_leaf.read_id == 'b'
    assert internal_node.filter.contains('ABC')
    assert internal_node.filter.contains('BCD')
    assert internal_node.filter.contains('EFG')
    assert internal_node.filter.contains('FGH')
    assert not read_1_leaf.filter.contains('EFG')
    assert not read_1_leaf.filter.contains('FGH')
    assert not read_2_leaf.filter.contains('ABC')
    assert not read_2_leaf.filter.contains('BCD')


def test_two_read_queries():
    """
    Ensures that we can query correctly through an internal node
    and that changing theta works accordingly
    """
    cuckoo_tree = CuckooBitTree(0.3, 3, 10, 8, 4, 500)
    # note: have 1  3mer in common
    read_1 = Read('a.fastq', 'a', None, 'ABCDE', 'IIII')
    read_2 = Read('b.fastq', 'b', None, 'CDEFG', 'IIII')
    cuckoo_tree.insert(read_1)
    cuckoo_tree.insert(read_2)
    assert cuckoo_tree.query('AAAAA') == []
    assert cuckoo_tree.query('BCDEF') == ['a', 'b']
    assert cuckoo_tree.query('CDEFG') == ['a', 'b']
    assert cuckoo_tree.query('ABCDE') == ['a', 'b']
    cuckoo_tree.theta = 0.6
    assert cuckoo_tree.query('AAAAA') == []
    assert cuckoo_tree.query('BCDEF') == ['a', 'b']
    assert cuckoo_tree.query('CDEFG') == ['b']
    assert cuckoo_tree.query('ABCDE') == ['a']
    cuckoo_tree.theta = 0.9
    assert cuckoo_tree.query('AAAAA') == []
    assert cuckoo_tree.query('BCDEF') == []
    assert cuckoo_tree.query('CDEFG') == ['b']
    assert cuckoo_tree.query('ABCDE') == ['a']


def test_two_internal_nodes():
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    read_1 = Read('a.fastq', 'a', None, 'ABCD', 'IIII')
    read_2 = Read('b.fastq', 'b', None, 'EFGH', 'IIII')
    read_3 = Read('c.fastq', 'c', None, 'ZABC', 'IIII')
    cuckoo_tree.insert(read_1)
    cuckoo_tree.insert(read_2)
    cuckoo_tree.insert(read_3)
    root = cuckoo_tree.root
    assert root.parent is None
    assert root.num_children() == 2
    assert root.read_id is None
    left_internal = root.children[0]
    assert left_internal.read_id is None
    assert left_internal.num_children() == 2
    assert left_internal.filter.num_items_in_filter == 3
    right_leaf = root.children[1]
    assert right_leaf.read_id == 'b'
    left_most_read = left_internal.children[0]
    right_read = left_internal.children[1]
    assert left_most_read.parent == left_internal
    assert left_most_read.children == []
    assert right_read.parent == left_internal
    assert right_read.children == []


def test_best_child_selection():
    cuckoo_tree = CuckooBitTree(0.5, 3, 10, 8, 4, 500)
    read_1 = Read('a.fastq', 'a', None, 'ABCD', 'IIII')
    read_2 = Read('b.fastq', 'b', None, 'EFGH', 'IIII')
    read_3 = Read('c.fastq', 'c', None, 'ZABC', 'IIII')
    read_4 = Read('d.fastq', 'd', None, 'ABCD', 'IIII')
    cuckoo_tree.insert(read_1)
    cuckoo_tree.insert(read_2)
    cuckoo_tree.insert(read_3)
    cuckoo_tree.insert(read_4)
    # b shares no kmers with other side
    assert cuckoo_tree.root.children[1].read_id == 'b'
    assert cuckoo_tree.root.children[1].children == []
    assert cuckoo_tree.root.children[1].parent == cuckoo_tree.root

    # read c has 1 different kmer than a and d
    left_subtree = cuckoo_tree.root.children[0]
    assert left_subtree.read_id is None
    assert left_subtree.num_children() == 2
    assert left_subtree.children[1].read_id == 'c'

    # a and d should have same parent since they have same info
    left_left_subtree = left_subtree.children[0]
    assert left_left_subtree.read_id is None
    assert left_left_subtree.filter.num_items_in_filter == 2
    assert left_left_subtree.children[0].read_id == 'a'
    assert left_left_subtree.children[1].read_id == 'd'
