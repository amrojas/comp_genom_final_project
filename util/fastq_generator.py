import argparse
from random import choice

def generate_reads(args):
    with open(args.output, "w") as f:
        for line in range(args.entries):
            f.write(">%05d/1\n" % line)
            f.write("".join(choice(['A', 'C', 'G', 'T']) for i in range(args.read_length)))
            f.write("\n+\n" + '!'*args.read_length + "\n")
    print("File {} written".format(args.output))

            

def arguments():
    usg = '''
        fastq_generator.py [-h] [-o DATAFILE1.FASTQ] [-e NUM_OF_READS] [-l READ_LENGTH]
               
    '''
    parser = argparse.ArgumentParser(description='Synthetic FASTQ generator', usage=usg)
    parser.add_argument('-o', dest='output', default="synthetic.fastq",
                        help='Output file name.')
    parser.add_argument("-e", dest='entries', type=int, default=5000, help="Number of read entries in file. Default=5000")
    parser.add_argument("-l", dest='read_length', help="Read length. Default=100", default=100, type=int)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arguments()
    generate_reads(args)