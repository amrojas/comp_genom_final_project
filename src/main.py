import argparse
import cuckoo_filter

from read import Read
from config import *

read_list = []
cuckooFilter = None

def create_cuckoo_filter(args):
    global cuckooFilter
    print("Creating the sketch. This might take a while ...")
    cuckooFilter = cuckoo_filter.CuckooFilter(NUM_BUCKETS, FP_SIZE, BUCKET_SIZE, MAX_ITER)
    if args.k == 0:
        for read in read_list:
            cuckooFilter.insert(read.line)
        print("Cuckoo filter created without splitting the reads into k-mers")
    else:
        for read in read_list:
            for i in range(len(read.line) - args.k):
                cuckooFilter.insert(read.line[i:i+args.k])
        print("Cuckoo filter created with kmers of size {}".format(args.k))

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

def cli(args):
    command = input("\nCLI: Please select \n 1) Create Cuckoo filter \n 2) Create Cuckoo tree \n 3) Query \n 4) Exit\n $$ ").strip()
    if command == "1":
        create_cuckoo_filter(args)
    elif command == "2":
        create_cuckoo_tree()
    elif command == "3":
        query(input("Enter the query phrase: "))
    elif command == "4":
        exit(0)
    cli(args)




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
        print("File {} read into memory".format(filename))

    # print(read_list[:20])
    if args.interactive:
        cli(args)

            

def arguments():
    usg = '''
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive] [--k Kmer_size]
               
    '''
    parser = argparse.ArgumentParser(description='Cuckoo Filter Tree Implementation', usage=usg)
    parser.add_argument('--datafiles', dest='datafiles', nargs="+", required=True,
                        help='The input file to populate the data structures')
    parser.add_argument("--interactive", help="Start CLI after reading files", action='store_true')
    parser.add_argument("-k", help="k-mer size, omit to disable kmer processing.", default=0, type=int)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arguments()
    initiate(args)