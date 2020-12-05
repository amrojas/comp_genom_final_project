# Evaluation scripts

This directory contains the bash scripts for evaluating the various data structures implemented.
The numbers used to represent each experiment are borrowed from the "Cuckoo Filter: Practically Better Than Bloom" paper.

## Reproduction Instructions

Assuming that you have already gone through the main README and installed the dependencies, you can continue here to create synthetic datasets and do the evaluation experiments.

### Creating the datasets

We use two different set of FASTQ files for the experiments. The majority of the experiments are done using  a rather large dataset containing 10M reads of 100 bases long. 
To create the large dataset, in the root directory of the project issue:

```bash
python3 util/fastq_generator.py -e 10000000 -o synthetic-large.fastq
```

To evaluate the tree structured sketches, we create four datasets each containing 10K reads of 100 bases long. Those can be created using:

```bash
python3 util/fastq_generator.py -e 10000 -o synthetic-tiny1.fastq
python3 util/fastq_generator.py -e 10000 -o synthetic-tiny2.fastq
python3 util/fastq_generator.py -e 10000 -o synthetic-tiny3.fastq
python3 util/fastq_generator.py -e 10000 -o synthetic-tiny4.fastq
```

### Running the scripts

#### EXP2
This experiment runs a parameter analysis on teh cuckoo filters. We test different combinations of bucket size, # of buckets, fingerprint size and stash. The output of the script is a number of timestamped csv files containing the performance metrics of the filter. Simply run:

```bash
./eval/exp2.sh
```

