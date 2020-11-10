from typing import List, Optional, Deque
from cuckoo_filter import CuckooFilter
from collections import deque
from read import Read


class CuckooTree:

    def __init__(self, theta, k, num_buckets, fp_size, bucket_size, max_iter):
        """
        Wrapper around the Node structure of tree for inserting, querying
        :param theta: Parameter to determine strictness of querying
        :param k: Size of kmer
        :param num_buckets: Parameter for CuckooFilter
        :param fp_size: Parameter for CuckooFilter
        :param bucket_size: Parameter for CuckooFilter
        :param max_iter: Parameter for CuckooFilter
        """
        self.root: Optional[Node] = None
        self.theta: float = theta
        self.k: int = k
        self.num_buckets = num_buckets
        self.fp_size = fp_size
        self.bucket_size = bucket_size
        self.max_iter = max_iter

    def insert(self, read: Read) -> None:
        """
        Creates a new node from this read and adds it into the tree
        :param read: the read information
        :return: None
        """
        node_to_insert = Node(self.k, self.num_buckets, self.fp_size, self.bucket_size, self.max_iter)
        node_to_insert.populate_read_info(read)

        if self.root is None:
            self.root = node_to_insert
            return

        parent = None
        current = self.root
        while current:
            if current.num_children() == 0:
                """
                current is a leaf representing a read, so
                create a new parent that contains node_to_insert
                and current as children
                """
                new_parent = Node(self.k, self.num_buckets, self.fp_size, self.bucket_size, self.max_iter)
                new_parent.parent = parent

                # todo: insert kmers from current and node_to_insert into new parent

                current.parent = new_parent
                node_to_insert.parent = new_parent

                new_parent.children.append(current)
                new_parent.children.append(node_to_insert)
                if parent is None:
                    # current is root -> new_parent is now root
                    self.root = new_parent
                    return
                else:
                    # Set new_parent as child of old parent
                    idx = parent.children.index(current)
                    parent.children[idx] = new_parent
                    return
            elif current.num_children() == 1:
                # todo: add kmers to current
                current.children.append(node_to_insert)
                return
            elif current.num_children() == 2:
                """
                TODO: how are we going to
                decide which side to go into
                In the paper it is just
                based on the bloom filter
                similarity, but we don't have that
                same property.
                We may have to try out some different stuff here.
                My first thought
                """
                # todo: add kmers to current
                parent = current
                current = current.children[0]
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
            if total_kmers_found > self.theta * total_kmers:
                for child in current.children:
                    nodes_to_explore.append(child)
                if current.num_children() == 0:
                    out.append(current.read_id)
        return out


class Node:

    def __init__(self, k, num_buckets, fp_size, bucket_size, max_iter):
        """
        Represents a single node of Cuckoo Tree.

        """
        self.children: List[Node] = []
        self.parent: Optional[Node] = None
        self.filter = CuckooFilter(num_buckets, fp_size, bucket_size, max_iter)

        self.read_id: Optional[str] = None
        self.k = k

    def populate_read_info(self, read: Read) -> None:
        self.read_id = read.id
        for kmer in read.kmers(self.k):
            self.filter.insert(kmer)

    def num_children(self) -> int:
        return len(self.children)


def kmers_in_string(string: str, k):
    for i in range(len(string) - k):
        yield string[i:i + k]
