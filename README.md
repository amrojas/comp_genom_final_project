# comp_genom_final_project
Repository for Cuckoo Tree Final Project

## Usage 
```
usage: 
        main.py [-h] [--datafiles DATAFILE1.FASTQ
         DATAFILE2.FASTQ ...] [--interactive] [--k Kmer_size]
               
    

Queuing System Simulation Software

optional arguments:
  -h, --help            show this help message and exit
  --datafiles DATAFILES [DATAFILES ...]
                        The input file to populate the data structures
  --interactive         Start CLI after reading files
  -k K                  k-mer size, omit to disable kmer processing.
```

## FASTQ Generator
To create random reads, use the Python script in the 'util' directory to create arbitrary sized FASTQ files.

Usage:
```
        fastq_generator.py [-h] [-o DATAFILE1.FASTQ] [-e NUM_OF_READS] [-l READ_LENGTH]
```
Default values for the arguments are 'synthetic.fastq', 5000 and 100 respectively.