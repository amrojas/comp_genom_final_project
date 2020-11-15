# comp_genom_final_project
Repository for Cuckoo Tree Final Project

## Usage 
```
usage: 
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive | --create-cuckoo-filter | --create-bloom-filter] 
            [-b buckets] [-f fp_size] [-s bucket_size] [-i iterations] [-k Kmer_size] [-e expected_#_items] [-p false_positive_probability]
            [--stash STASH_SIZE] [--auto] [-v]
    

Cuckoo Filter Tree Implementation

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
  --stash STASH         CuckooFilter; Stash size. Default=0
  --auto                CuckooFilter; Automatically derive the fp_size,
                        bucket_size and num of buckets from fp_probability and
                        expected items.
  --create-cuckoo-filter
                        Create the cuckoo filter, measure and report the
                        statistics, then exit.
  --create-bloom-filter
                        Create the Bloom filter, measure and report the
                        statistics, then exit.
```

## FASTQ Generator
To create random reads, use the Python script in the 'util' directory to create arbitrary sized FASTQ files.

Usage:
```
        fastq_generator.py [-h] [-o DATAFILE1.FASTQ] [-e NUM_OF_READS] [-l READ_LENGTH]
```
Default values for the arguments are 'synthetic.fastq', 5000 and 100 respectively.

## Experiment scripts
In the `eval` directory, you can find a bash script for executing the `main.py` driver with different parameters. The results are saved as a timestamped csv file in the same directory. The csv file can be input to the provided matplotlib script to generate the plots. Note that the plotting script will need to be adjusted according to the parameters/results.