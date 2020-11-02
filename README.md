# comp_genom_final_project
Repository for Cuckoo Tree Final Project

## Usage 
```
usage: 
        main.py [-h] [--datafiles DATAFILE1.FASTQ DATAFILE2.FASTQ ...] [--interactive | --create-cuckoo-filter] 
            [-b buckets] [-f fp_size] [-s bucket_size] [-i iterations] [-k Kmer_size]
    

Cuckoo Filter Tree Implementation

optional arguments:
  -h, --help            show this help message and exit
  --datafiles DATAFILES [DATAFILES ...]
                        The input file to populate the data structures
  --interactive         Start CLI after reading files
  -k K                  k-mer size, omit to disable kmer processing.
  -b B                  Number of buckets. Default=6500
  -f F                  Fingerprint size. Default=16
  -s S                  Bucket size. Default=64
  -i I                  Max iterations befor insertion fails. Default=500
  --create-cuckoo-filter
                        Create the cuckoo filter, measure the creation time
                        and load factor, then exit.
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