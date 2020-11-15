import argparse
import cuckoo_filter
import time
from sys import getsizeof

from read import Read
from config import *

read_list = []
cuckooFilter = None

def print_stats(filter_stats, sketch_config, verbose=False):
    if verbose:
        print("k,buckets,fp_size,buck_size,iterations,items,constr_speed,load_factor, total_size_bytes, bits_per_item, false_positive_rate")
    print("{},{},{},{},{},{},{:.4f},{},{},{},{}".format(sketch_config.k,sketch_config.num_buckets,sketch_config.fp_size,
        sketch_config.bucket_size,sketch_config.max_iter, filter_stats["items"], filter_stats["constr_speed"],
        filter_stats["load_factor"], filter_stats["total_size"], filter_stats["bpi"], filter_stats["fp_rate"]))

def create_cuckoo_filter(sketch_config, filter_stats):
    global cuckooFilter
    # print("Creating the sketch. This might take a while ...")
    if sketch_config.stash != 0:
        cuckooFilter = cuckoo_filter.CuckooFilterStash(sketch_config.num_buckets, 
            sketch_config.fp_size, sketch_config.bucket_size, sketch_config.max_iter, sketch_config.stash)
    else:
        cuckooFilter = cuckoo_filter.CuckooFilter(sketch_config.num_buckets, sketch_config.fp_size, 
            sketch_config.bucket_size, sketch_config.max_iter)
    items = 0
    start = time.time()
    if sketch_config.k == 0:
        for read in read_list:
            if cuckooFilter.insert(read.line) == False:
                break
            items+=1
    else:
        failed = False
        r = 0
        while not failed and r < len(read_list):
            for i in range(len(read_list[r].line) - sketch_config.k):
                if cuckooFilter.insert(read_list[r].line[i:i+sketch_config.k]) == False:
                    failed = True
                    break
                items+=1
    end = time.time()
    filter_stats["items"] = items
    filter_stats["constr_speed"] = items / (end-start)
    filter_stats["load_factor"] = items / (sketch_config.num_buckets * sketch_config.bucket_size)
    filter_stats["total_size"] = cuckooFilter.get_size()
    filter_stats["bpi"] = (filter_stats["total_size"] / items) * 8


def create_cuckoo_tree():
    raise NotImplementedError

def query(q):
    global cuckooFilter
    if cuckooFilter == None:
        print("cuckoo filter is empty.")
        return -1
    if cuckooFilter.contains(q):
        print("POSITIVE")
        return 1
    else:
        print("NEGATIVE")
        return 0

def cli(args, sketch_config, filter_stats):
    command = input("\nCLI: Please select \n 1) Create Cuckoo filter \n 2) Create Cuckoo tree \n 3) Query \n 4) Exit\n $$ ").strip()
    if command == "1":
        create_cuckoo_filter(sketch_config, filter_stats)
        print_stats(filter_stats, sketch_config, args.verbose)
    elif command == "2":
        create_cuckoo_tree()
    elif command == "3":
        query(input("Enter the query phrase: "))
    elif command == "4":
        exit(0)
    cli(args, sketch_config, filter_stats)


def initiate(args):
    for filename in args.datafiles:
        line_ptr = 0
        with open(filename, "r") as f:
            while True:
                read_id = f.readline()[1:-1]
                if read_id == "":
                    break
                read_line = f.readline().strip()
                temp = f.readline()
                read_quality = f.readline()
                read_list.append(Read(filename, read_id, line_ptr, read_line, read_quality))
                line_ptr+=1
        # print("File {} read into memory".format(filename))

    # print(read_list[:20])
    sketch_config = SketchConfig(args.b, args.f, args.s, args.i, args.k, args.stash)
    filter_stats = {
        "items" : 0,
        "constr_speed" : 0.0,
        "load_factor": 0.0,
        "total_size": 0,
        "bpi": 0,
        "fp_rate" : 0
    }
    if args.interactive:
        cli(args, sketch_config, filter_stats)
    elif args.create_cuckoo_filter:
        create_cuckoo_filter(sketch_config, filter_stats)
        print_stats(filter_stats, sketch_config, args.verbose)



def arguments():
    usg = '''
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive | --create-cuckoo-filter] 
            [-b buckets] [-f fp_size] [-s bucket_size] [-i iterations] [-k Kmer_size] [--stash STASH_SIZE] [-v]
    '''
    parser = argparse.ArgumentParser(description='Cuckoo Filter Tree Implementation', usage=usg)
    parser.add_argument('--datafiles', dest='datafiles', nargs="+", required=True,
                        help='The input file to populate the data structures')
    parser.add_argument("--interactive", help="Start CLI after reading files", action='store_true')
    parser.add_argument("-v", help="Verbose: Prints the labels for output stats.", dest="verbose", action='store_true')
    parser.add_argument("-k", help="k-mer size, omit to disable kmer processing.", default=0, type=int)
    parser.add_argument("-b", help="Number of buckets. Default=6500", default=6500, type=int)
    parser.add_argument("-f", help="Fingerprint size. Default=16", default=16, type=int)
    parser.add_argument("-s", help="Bucket size. Default=64", default=64, type=int)
    parser.add_argument("-i", help="Max iterations befor insertion fails. Default=500", default=500, type=int)
    parser.add_argument("--stash", help="Stash size. Default=10", default=10, type=int)
    parser.add_argument("--create-cuckoo-filter", help="Create the cuckoo filter, measure the creation time and load factor, then exit.", action='store_true')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arguments()
    initiate(args)
