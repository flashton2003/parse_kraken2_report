import os
# import pandas as pd
from anytree import Node, RenderTree

class Taxon():
    def __init__(self, split_line):
        self.percent_reads_mapped = float(split_line[0])
        self.number_reads_rooted_here = int(split_line[1])
        self.number_reads_assigned_here = int(split_line[2])
        self.rank = split_line[3]
        self.ncbi_id = int(split_line[4])
        self.name = split_line[5].strip()

# def my_sum(arg):
#     total = 0
#     for val in arg:
#         total += val
#     return total

def read_kraken_report(inhandle):
    # kraken_report = pd.read_csv(inhandle, sep='\t', header=None)
    kraken_report_taxa = []
    with open(inhandle) as fi:
        for line in fi.readlines():
            split_line = line.strip().split('\t')
            taxon = Taxon(split_line)
            # print(vars(taxa))
            kraken_report_taxa.append(taxon)
    

    # return kraken_report

def convert_report_to_tree(kraken_report):
    '''
    1. go thorugh the report lines
    2. if the line has more than 0.05% of the reads, consider it for inclusion in the output
    3. only include it in the output if there isn't an entry below it in the taxonomic level which 
    '''
    root = Node('root')
    '''
    current_level = 0
    for line in report:
        if line.level > current_level:
            node("Name", parent = current_level)


    '''


def parse_tree(kraken_tree):
    '''
    1. find all nodes without children (i.e. tips)
    2. take path between each tip and root
    3. go up the path towards the root until get to 
    '''
    pass

def main(inhandle):
    '''
    1. read in kraken report
    2. parse the report
    '''
    tax_levels = ['U', 'R', 'D', 'K', 'P', 'C', 'O', 'F', 'G', 'S']
    kraken_report = read_kraken_report(inhandle)
    # parse_report(kraken_report)

inhandle = '/Users/flashton/Dropbox/GordonGroup/ben_kumwenda_genomes/kraken2/results/2020.09.30/18080-1-FR10242277.kraken_report.txt'

assert os.path.exists(inhandle)

if __name__ == '__main__':
    main(inhandle)