from typing import List, Optional, Deque
from bloom_filter import BloomFilter
from collections import deque
from read import Read
from copy import deepcopy
from bitarray import bitarray
from bitarray.util import count_xor
import sys


class BloomTree:

    def __init__(self, theta, k, expected_num, fp_prob):
        """
        Wrapper around the Node structure of tree for inserting, querying
        :param theta: Parameter to determine strictness of querying
        :param k: Size of kmer
        :param expected_num: Bloom Filter parameter
        :param fp_prob: Bloom Filter parameter
        """
        self.root: Optional[Node] = None
        self.theta: float = theta
        self.k: int = k
        self.expected_num = expected_num
        self.fp_prob = fp_prob
        self.aggregate_size = self.get_insternal_size()

    def insert(self, dataset: List[Read]) -> bool:
        """
        Creates a new node from this dataset and inserts it into the tree
        :return: None
        """
        node_to_insert = Node(self.k, self.expected_num, self.fp_prob)
        node_to_insert.populate_dataset_info(dataset)
        self.aggregate_size += node_to_insert.get_size()

        if self.root is None:
            self.root = node_to_insert
            return True

        parent = None
        current = self.root
        while current:
            if current.num_children() == 0:
                """
                current is a leaf representing a dataset, so
                create a new parent that contains node_to_insert
                and current as children
                """
                new_parent = Node(self.k, self.expected_num, self.fp_prob)
                new_parent.parent = parent
                self.aggregate_size += new_parent.get_size()

                # Kmers from existing and new leaf
                new_parent.filter.filter = bitarray(current.filter.filter)
                new_parent.add_node_kmers(node_to_insert)

                # Set appropriate parent/child pointers
                current.parent = new_parent
                node_to_insert.parent = new_parent
                new_parent.children.append(current)
                new_parent.children.append(node_to_insert)

                # Special case where root is a leaf
                if parent is None:
                    # current is root -> new_parent is now root
                    self.root = new_parent
                    return True

                # Set new_parent as child of old parent
                idx = parent.children.index(current)
                parent.children[idx] = new_parent
                return True
            elif current.num_children() == 1:
                # insert kmers
                current.add_node_kmers(node_to_insert)

                # we found an empty slot to insert into
                current.children.append(node_to_insert)
                return True
            elif current.num_children() == 2:
                # insert kmers
                current.add_node_kmers(node_to_insert)

                # select "best" child
                score_0 = current.children[0].score(node_to_insert)
                score_1 = current.children[1].score(node_to_insert)
                best_child = 0 if score_0 < score_1 else 1

                # recur
                parent = current
                current = current.children[best_child]

        raise Exception("Did not insert successfully!")

    def query(self, query: str) -> List[str]:
        """
        Perform a DFS of the tree and collects reads that
        pass similarity test.
        :param query: The query string to be broken into kmers
        :return: The list of read_ids that "match"
        """
        nodes_to_explore: Deque[Node] = deque()
        nodes_to_explore.append(self.root)

        out: List[str] = []
        while nodes_to_explore:
            current = nodes_to_explore.popleft()
            total_kmers_found = 0
            total_kmers = 0
            for kmer in kmers_in_string(query, self.k):
                if current.filter.contains(kmer):
                    total_kmers_found += 1
                total_kmers += 1
            if total_kmers_found >= self.theta * total_kmers:
                for child in current.children:
                    nodes_to_explore.append(child)
                if current.num_children() == 0:
                    out.append(current.dataset_id)
        return out

    def contains(self, query):
        """
        A wrapper for backward comptibility with other data structure implementations
        """
        return self.query(query)

    def get_insternal_size(self):
        """
        Returns the total number of bytes occupied by the filter object
        """
        return (
                sys.getsizeof(self.theta) +
                sys.getsizeof(self.expected_num) +
                sys.getsizeof(self.fp_prob) +
                sys.getsizeof(self.k) +
                sys.getsizeof(self.root)
        )


class Node:

    def __init__(self, k, expected_num, fp_prob):
        """
        Represents a single node of Bloom Tree

        """
        self.children: List[Node] = []
        self.parent: Optional[Node] = None
        self.filter = BloomFilter(expected_num, fp_prob)

        self.dataset_id: Optional[str] = None
        self.k = k

    def populate_dataset_info(self, dataset: List[Read]) -> None:
        self.dataset_id = dataset[0].filename
        self.insert_kmers_from_dataset(dataset)

    def insert_kmers_from_dataset(self, dataset: List[Read]) -> None:
        for read in dataset:
            for kmer in read.kmers(self.k):
                self.filter.insert(kmer)

    def add_node_kmers(self, other: 'Node') -> None:
        self.filter.filter |= other.filter.filter

    def num_children(self) -> int:
        return len(self.children)

    def score(self, other: 'Node') -> int:
        """
        "Hamming distance" score where lower is better
        :param other: The node to compare against
        """
        return count_xor(self.filter.filter, other.filter.filter)

    def get_size(self):
        """
        Returns the total number of bytes occupied by the filter object
        """
        return (
                sys.getsizeof(self.children) +
                sys.getsizeof(self.parent) +
                sys.getsizeof(self.dataset_id) +
                sys.getsizeof(self.k) +
                self.filter.get_size()
        )


def kmers_in_string(string: str, k):
    for i in range(len(string) - k + 1):
        yield string[i:i + k]
