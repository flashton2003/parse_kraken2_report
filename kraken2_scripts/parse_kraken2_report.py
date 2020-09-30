import os
import string
# import pandas as pd
from anytree import Node, RenderTree

class Taxon():
    def __init__(self, split_line):
        self.percent_reads_assigned = float(split_line[0])
        self.number_reads_rooted_here = int(split_line[1])
        self.number_reads_assigned_here = int(split_line[2])
        self.full_rank = split_line[3]
        self.rank = self.full_rank.rstrip(string.digits)
        self.ncbi_id = int(split_line[4])
        self.name = split_line[5].strip()

def read_kraken_report(inhandle):
    kraken_report_taxa = []
    with open(inhandle) as fi:
        for line in fi.readlines():
            split_line = line.strip().split('\t')
            # print(split_line)
            taxon = Taxon(split_line)
            kraken_report_taxa.append(taxon)
    return kraken_report_taxa

def convert_report_taxa_to_tree(kraken_report, taxa_levels):
    '''
    1. go thorugh the report lines
    2. if the line has more than 0.05% of the reads, consider it for inclusion in the output
    3. only include it in the output if there isn't an entry below it in the taxonomic level which 
    '''
    assert kraken_report[0].name == 'unclassified'
    assert kraken_report[1].name == 'root'
    root = Node('root', percent_reads_assigned = kraken_report[1].percent_reads_assigned)
    current_level = 1
    for taxon in kraken_report[3:]:
        if taxa_levels.index(taxon.full_rank) > current_level:
            Node(taxon.name, parent = root)



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

def main(inhandle, taxa_levels):
    '''
    1. read in kraken report
    2. parse the report
    '''
    
    kraken_report_taxa = read_kraken_report(inhandle)
    convert_report_taxa_to_tree(kraken_report_taxa, taxa_levels)
    # parse_report(kraken_report)

inhandle = '/Users/flashton/Dropbox/GordonGroup/ben_kumwenda_genomes/kraken2/results/2020.09.30/18080-1-FR10242277.kraken_report.txt'
taxa_levels = ['U', 'R', 'R1', 'D', 'D1', 'K', 'P', 'C', 'O', 'F', 'G', 'G1', 'S']

assert os.path.exists(inhandle)

if __name__ == '__main__':
    main(inhandle, taxa_levels)