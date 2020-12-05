# Computational Genomics Final project artifacts for group #64
This repository contains the source codes as well as the evaluation scrips for building different variants of Bloom and Cuckoo filters and evaluating them.
## Usage 
```
usage: 
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive | --create-cuckoo-filter | --create-cuckoo-filter-bit |
            --create-bloom-filter | --create-bloom-tree | --create-cuckoo-tree] [-q QUERY_FILE] [--fp-query] [--query-tput]
            [-b buckets] [-f fp_size] [-s bucket_size] [-i iterations] [-k Kmer_size] [-e expected_#_items] [-p false_positive_probability]
            [--stash STASH_SIZE] [--auto] [-v]
    

Cuckoo/Bloom Filter variants Implementation

optional arguments:
  -h, --help            show this help message and exit
  --datafiles DATAFILES [DATAFILES ...]
                        The input file to populate the data structures
  --interactive         Start CLI after reading files
  -v                    Verbose: Prints the labels for output stats.
  -k K                  k-mer size, omit to disable kmer processing.
  -b B                  CuckooFilter; Number of buckets. Default=6500
  -f F                  CuckooFilter; Fingerprint size. Default=16
  -s S                  CuckooFilter; Bucket size. Default=64
  -i I                  CuckooFilter; Max iterations befor insertion fails.
                        Default=500
  -e E                  CuckooFilterAuto&BloomFilter; Expected number of
                        items. Default=10000
  -p P                  CuckooFilterAuto&BloomFilter; False positive
                        probability. Default=0.001
  -t T                  BloomTree; Strictness of querying. Default=0.5
  -q Q                  Query file
  --stash STASH         CuckooFilter; Stash size. Default=0
  --auto                CuckooFilter; Automatically derive the fp_size,
                        bucket_size and num of buckets from fp_probability and
                        expected items.
  --create-cuckoo-filter
                        Create the cuckoo filter, measure and report the
                        statistics, then exit.
  --create-cuckoo-filter-bit
                        Create the bitarray variant of cuckoo filter, measure
                        and report the statistics, then exit.
  --create-bloom-filter
                        Create the Bloom filter, measure and report the
                        statistics, then exit.
  --create-bloom-tree   Create the Bloom tree, measure and report the
                        statistics, then exit.
  --create-cuckoo-tree  Create the Bloom cuckoo, measure and report the
                        statistics, then exit.
  --fp-query            Perform false positive queries after creating the
                        sketch, report FP rate then exit.
  --query-tput          Perform queries after creating the sketch, report
                        query throughput then exit.
  --insert-tput         Perform insertion throughput measurements.
```

To be as generic as possible, we included all the parameters as command line arguments. For example the below command will create bit-array variant of the cuckoo filter from the synthetic-large.fastq dataset and uses the expected number of items (10M) and the false_positive probability (0.01) to derive the number of buckets, bucket size and fingerprint size.
```
python3 src/main.py --datafiles synthetic-large.fastq --create-cuckoo-filter-bit --auto -e 10000000 -p 0.01 -v
```

`--fp-query`, `query-tput` and `--insert-tput` are optional flags used in the evaluation. Refer to the evaluation scripts for exmples on how to use these flags.

Use `-v` to print the description of the output numbers. Also at each run, only one of the `--create-` flags must be provided.

To create a Sequence Bloom tree, execute:

```
python3 src/main.py --datafiles synthetic-tiny1.fastq synthetic-tiny2.fastq synthetic-tiny3.fastq synthetic-tiny4.fastq --create-bloom-tree  -e 500000 -p 0.01 -k 20 -v
```

## Unit tests
The `test\` directory contains various test cases for the implementation. Run the below command to execute all the unittests provided:

```
python3 -m pytest
```

## FASTQ Generator
To create random reads, use the Python script in the 'util' directory to create arbitrary sized FASTQ files.

Usage:
```
        fastq_generator.py [-h] [-o DATAFILE1.FASTQ] [-e NUM_OF_READS] [-l READ_LENGTH]
```
Default values for the arguments are 'synthetic.fastq', 5000 and 100 respectively.

## False-positive dataset generator
We use a simple brute-force algorithm to compare a query dataset to the main dataset and extract all the reads that are not present in the main dataset.

```
usage: 
        false_positive_dataset_generator.py [-h] [-o OUTPUT.FASTQ] [-p PRIMARY_DATASET] [-c CANDIDATE_DATASET]
               
    

False positive FASTQ generator

optional arguments:
  -h, --help    show this help message and exit
  -o OUTPUT     Output file name.
  -p PRIMARY    Dataset used for sketching.
  -c CANDIDATE  Candidate dataset to fetch fp candidate reads.
```


## Experiment scripts
In the `eval` directory, you can find a bash script for executing the `main.py` driver with different parameters. The results are saved as a timestamped csv file in the same directory. The csv file can be input to the provided matplotlib script to generate the plots. Note that the plotting script will need to be adjusted according to the parameters/results.

## Reproduction Instructions

### Collecting the requirements
We use Python3, so the requirements can be installed using the below command issued in the root of the project:

```
pip3 install -r requirements.txt --user
```

## Running the experiments

To perform the experiments, refer to the readme file in the `eval/` directory.

## Contributors

- Omar Ahmed
- Andrew Rojas
- Erfan Sharafzadeh
- Kathleen Newcomer