import argparse
import cuckoo_filter
import bloom_filter
import time
from sys import getsizeof

from read import Read
from config import *

read_list = []
cuckooFilter = None
bloomFilter = None

def print_stats(filter_stats, sketch_config, verbose=False):
    if verbose:
        print("k,buckets,fp_size,buck_size,iterations,items,constr_speed,load_factor, total_size_bytes, bits_per_item, false_positive_rate")
    print("{},{},{},{},{},{},{:.4f},{},{},{},{}".format(sketch_config.k,sketch_config.num_buckets,sketch_config.fp_size,
        sketch_config.bucket_size,sketch_config.max_iter, filter_stats["items"], filter_stats["constr_speed"],
        filter_stats["load_factor"], filter_stats["total_size"], filter_stats["bpi"], filter_stats["fp_rate"]))

def create_bloom_filter(sketch_config, filter_stats):
    global bloomFilter
    insertion_tput_records = []
    # print("Creating the sketch. This might take a while ...")
    bloomFilter = bloom_filter.BloomFilter(sketch_config.expected_items, sketch_config.fp_prob)
    items = 0
    load_factor_step_size = bloomFilter.expected_num / 10
    step = 1
    start = time.time()
    if sketch_config.k == 0:
        t1 = time.time()
        for read in read_list:
            if bloomFilter.insert(read.line) == False:
                break
            items+=1
            if items >= load_factor_step_size*step:
                    insertion_tput_records.append(load_factor_step_size/(time.time() - t1))
                    step +=1
                    t1 = time.time()
    else:
        failed = False
        r = 0
        t1 = time.time()
        while not failed and r < len(read_list):
            for i in range(len(read_list[r].line) - sketch_config.k):
                if bloomFilter.insert(read_list[r].line[i:i+sketch_config.k]) == False:
                    failed = True
                    break
                items+=1
                if items >= load_factor_step_size*step:
                    insertion_tput_records.append(load_factor_step_size/(time.time() - t1))
                    step +=1
                    t1 = time.time()
    end = time.time()
    filter_stats["items"] = items
    filter_stats["constr_speed"] = items / (end-start)
    filter_stats["load_factor"] = items / bloomFilter.expected_num
    filter_stats["total_size"] = bloomFilter.get_size()
    filter_stats["bpi"] = (filter_stats["total_size"] / items) * 8
    filter_stats["insertion_tput"] = insertion_tput_records

def create_cuckoo_filter(sketch_config, filter_stats):
    global cuckooFilter
    insertion_tput_records = []
    # print("Creating the sketch. This might take a while ...")
    if sketch_config.auto:
        sketch_config.num_buckets, sketch_config.fp_size, sketch_config.bucket_size = cuckoo_filter.get_cuckoo_filter_params(sketch_config.expected_items,
            sketch_config.fp_prob)
    if sketch_config.stash != 0:
        cuckooFilter = cuckoo_filter.CuckooFilterStash(sketch_config.num_buckets, 
            sketch_config.fp_size, sketch_config.bucket_size, sketch_config.max_iter, sketch_config.stash)
    if sketch_config.bitarray_variant:
        cuckooFilter = cuckoo_filter.CuckooFilterBit(sketch_config.num_buckets, sketch_config.fp_size, 
            sketch_config.bucket_size, sketch_config.max_iter)
    else:
        cuckooFilter = cuckoo_filter.CuckooFilter(sketch_config.num_buckets, sketch_config.fp_size, 
            sketch_config.bucket_size, sketch_config.max_iter)
    items = 0
    load_factor_step_size = (cuckooFilter.num_buckets * cuckooFilter.bucket_size) / 10
    step = 1
    start = time.time()
    if sketch_config.k == 0:
        t1 = time.time()
        for read in read_list:
            if cuckooFilter.insert(read.line) == False:
                break
            items+=1
            if items >= load_factor_step_size*step:
                insertion_tput_records.append(load_factor_step_size/(time.time() - t1))
                step +=1
                t1 = time.time()

    else:
        failed = False
        r = 0
        t1 = time.time()
        while not failed and r < len(read_list):
            for i in range(len(read_list[r].line) - sketch_config.k):
                if cuckooFilter.insert(read_list[r].line[i:i+sketch_config.k]) == False:
                    failed = True
                    break
                items+=1
                if items >= load_factor_step_size*step:
                    insertion_tput_records.append(load_factor_step_size/(time.time() - t1))
                    step +=1
                    t1 = time.time()
    end = time.time()
    filter_stats["items"] = items
    filter_stats["constr_speed"] = items / (end-start)
    filter_stats["load_factor"] = items / (cuckooFilter.num_buckets * cuckooFilter.bucket_size)
    filter_stats["total_size"] = cuckooFilter.get_size()
    filter_stats["bpi"] = (filter_stats["total_size"] / items) * 8
    filter_stats["insertion_tput"] = insertion_tput_records


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

def perform_fp_query(query_file, filter_stats, filter):
    line_ptr = 0.0
    positives = 0.0
    with open(query_file, "r") as f:
        while True:
            read_id = f.readline()[1:-1]
            if read_id == "":
                break
            read_line = f.readline().strip()
            temp = f.readline()
            read_quality = f.readline()
            if filter.contains(read_line):
                positives+=1
            line_ptr+=1
            if line_ptr == 100000:
                break
    if line_ptr == 0.0:
        print("WARNING! empty query file!")
        return
    filter_stats["fp_rate"] = positives/line_ptr

def cli(args, sketch_config, filter_stats):
    command = input("\nCLI: Please select \n 1) Create Cuckoo filter \n 2) Create Bloom filter \n 3) Create Cuckoo tree \n 4) Query \n 5) Create Cuckoo filter BitArray Variant 6) Exit\n $$ ").strip()
    if command == "1":
        create_cuckoo_filter(sketch_config, filter_stats)
        print_stats(filter_stats, sketch_config, args.verbose)
    elif command == "2":
        create_bloom_filter(sketch_config, filter_stats)
        print_stats(filter_stats, sketch_config, args.verbose)
    elif command == "3":
        create_cuckoo_tree()
    elif command == "4":
        query(input("Enter the query phrase: "))
    elif command == "5":
        
        sketch_config["bitarray_variant"] = True
    elif command == "6":
        exit(0)
    cli(args, sketch_config, filter_stats)


def initiate(args):
    global bloomFilter
    global cuckooFilter
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
    sketch_config = SketchConfig(args.b, args.f, args.s, args.i, args.k, args.stash, args.e, args.p, args.auto)
    filter_stats = {
        "items" : 0,
        "constr_speed" : 0.0,
        "load_factor": 0.0,
        "total_size": 0,
        "bpi": 0,
        "fp_rate" : 0,
        "insertion_tput": []
    }
    filter = None
    if args.interactive:
        cli(args, sketch_config, filter_stats)
    elif args.create_bloom_filter:
        create_bloom_filter(sketch_config, filter_stats)
        filter = bloomFilter
    elif args.create_cuckoo_filter:
        create_cuckoo_filter(sketch_config, filter_stats)
        filter = cuckooFilter
    elif args.create_cuckoo_filter_bit:
        sketch_config.bitarray_variant = True
        create_cuckoo_filter(sketch_config, filter_stats)
        filter = cuckooFilter
    if args.fp_query:
        perform_fp_query(args.q, filter_stats, filter)
    if args.insert_tput:
        print("Insertion Throuput at 0.1 increments of load factor: ", end=" ")
        for item in filter_stats["insertion_tput"]:
            print(item, sep=", ")
    print_stats(filter_stats, sketch_config, args.verbose)



def arguments():
    usg = '''
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive | --create-cuckoo-filter | --create-cuckoo-filter-bit |
            --create-bloom-filter] [-q QUERY_FILE] [--fp-query]
            [-b buckets] [-f fp_size] [-s bucket_size] [-i iterations] [-k Kmer_size] [-e expected_#_items] [-p false_positive_probability]
            [--stash STASH_SIZE] [--auto] [-v]
    '''
    parser = argparse.ArgumentParser(description='Cuckoo Filter Tree Implementation', usage=usg)
    parser.add_argument('--datafiles', dest='datafiles', nargs="+", required=True,
                        help='The input file to populate the data structures')
    parser.add_argument("--interactive", help="Start CLI after reading files", action='store_true')
    parser.add_argument("-v", help="Verbose: Prints the labels for output stats.", dest="verbose", action='store_true')
    parser.add_argument("-k", help="k-mer size, omit to disable kmer processing.", default=0, type=int)
    parser.add_argument("-b", help="CuckooFilter; Number of buckets. Default=6500", default=6500, type=int)
    parser.add_argument("-f", help="CuckooFilter; Fingerprint size. Default=16", default=16, type=int)
    parser.add_argument("-s", help="CuckooFilter; Bucket size. Default=64", default=64, type=int)
    parser.add_argument("-i", help="CuckooFilter; Max iterations befor insertion fails. Default=500", default=500, type=int)
    parser.add_argument("-e", help="CuckooFilterAuto&BloomFilter; Expected number of items. Default=10000", default=10000, type=int)
    parser.add_argument("-p", help="CuckooFilterAuto&BloomFilter; False positive probability. Default=0.001", default=0.001, type=float)
    parser.add_argument("-q", help="Query file", default="")
    parser.add_argument("--stash", help="CuckooFilter; Stash size. Default=0", default=0, type=int)
    parser.add_argument("--auto", help="CuckooFilter; Automatically derive the fp_size, bucket_size and num of buckets from fp_probability and expected items.", dest="auto", action='store_true')
    parser.add_argument("--create-cuckoo-filter", help="Create the cuckoo filter, measure and report the statistics, then exit.", action='store_true')
    parser.add_argument("--create-cuckoo-filter-bit", help="Create the bitarray variant of cuckoo filter, measure and report the statistics, then exit.", action='store_true')
    parser.add_argument("--create-bloom-filter", help="Create the Bloom filter, measure and report the statistics, then exit.", action='store_true')
    parser.add_argument("--fp-query", help="Perform false positive queries after creating the sketch, report FP rate then exit.", action='store_true')
    parser.add_argument("--insert-tput", help="Perform insertion throughput measurements.", action='store_true')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arguments()
    initiate(args)
