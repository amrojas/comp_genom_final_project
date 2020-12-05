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
This script takes around two hours to run and generates four csv files in the eval/ directory that can be used to create the figures 5.a to 5.d in the project writeup.

#### EXP3
This script generates the results presented in table 1, comparing Cuckoo filter variants to the Bloom filter. Note that this script needs another dataset called fp_dataset.fastq which contains reads that are NOT present in the main dataset and is used to measure the false positive rate for the indexes.
To create the fp_dataset.fastq file, first we generate a query dataset called `synthetic.fastq` which contains 100K reads. The using the `fals_positive_dataset_generator.py` script, we create the `fp_dataset.fastq`. The script uses brute force to compare all reads in the query dataset against the large dataset and outputs all the reads that are not in the large dataset. run:

```
python3 util/fastq_generator.py -e 100000 -o synthetic.fastq
python3 util/false_positive_dataset_generator.py -p synthetic-large.fastq -c synthetic.fastq
```

NOTE: We have provided the fp_dataset.fastq in the root directory.

#### EXP4

This script is used to measure the bits-per-item achieved among Bloom filters and two implementations of the Cuckoo filter using different fp_probability parametes. The results are presented in figure 6 of the write-up. Simply run:

```bash
./eval/exp4.sh
```

#### EXP7

This script is used to measure the insertion throughput among Bloom filters and two implementations of the Cuckoo filter. The results are presented in figure 7 of the write-up Simply run:

```bash
./eval/exp7.sh
```

#### EXP6

This script is used to measure the query throughput among Bloom filters and two implementations of the Cuckoo filter. The results are presented in figure 8 of the write-up. Simply run:

```bash
./eval/exp6.sh
```
