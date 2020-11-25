import argparse
from random import choice

read_list = []

def contains(l, item):
    for read in l:
        if read == item:
            return True
    return False

def generate_fpdataset(args):
    line_ptr = 0
    output = open(args.output, "w")
    with open(args.primary, "r") as f:
        while True:
            read_id = f.readline()[1:-1]
            if read_id == "":
                break
            read_line = f.readline().strip()
            temp = f.readline()
            read_quality = f.readline()
            read_list.append(read_line)
            line_ptr+=1
    with open(args.candidate, "r") as f:
        while True:
            read_id = f.readline()[1:-1]
            if read_id == "":
                break
            read_line = f.readline().strip()
            temp = f.readline()
            read_quality = f.readline()
            if not contains(read_list, read_line):
                output.write(">%05d/1\n" % line_ptr)
                output.write(read_line)
                output.write("\n+\n" + '!'*100 + "\n")
            line_ptr+=1
    print("File {} written".format(args.output))

            

def arguments():
    usg = '''
        false_positive_dataset_generator.py [-h] [-o OUTPUT.FASTQ] [-p PRIMARY_DATASET] [-c CANDIDATE_DATASET]
               
    '''
    parser = argparse.ArgumentParser(description='False positive FASTQ generator', usage=usg)
    parser.add_argument('-o', dest='output', default="fp_dataset.fastq",
                        help='Output file name.')
    parser.add_argument("-p", dest='primary', help="Dataset used for sketching.")
    parser.add_argument("-c", dest='candidate', help="Candidate dataset to fetch fp candidate reads.")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arguments()
    generate_fpdataset(args)