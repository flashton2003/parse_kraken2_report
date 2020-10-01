import os
import string
import argparse
from anytree import Node, RenderTree, PreOrderIter, Walker

class Taxon():
    def __init__(self, split_line, taxa_levels, sample_name):
        self.percent_reads_assigned = float(split_line[0])
        self.number_reads_rooted_here = int(split_line[1])
        self.number_reads_assigned_here = int(split_line[2])
        self.full_rank = split_line[3]
        self.rank = self.full_rank.rstrip(string.digits)
        self.taxonomic_level = taxa_levels.index(self.full_rank)
        self.ncbi_id = int(split_line[4])
        self.name = split_line[5].strip()
        self.sample_name = sample_name
        self.printed_already = False

    def print_info(self):
        print(self.sample_name, self.percent_reads_assigned, self.number_reads_rooted_here, self.number_reads_assigned_here, self.full_rank, self.ncbi_id, self.name, sep = '\t')


def read_kraken_report(inhandle, taxa_levels):
    assert isinstance(taxa_levels, list)
    sample_name = inhandle.split('/')[-1].split('.')[0]
    kraken_report_taxa = []
    with open(inhandle) as fi:
        for line in fi.readlines():
            split_line = line.strip().split('\t')
            # print(split_line)
            taxon = Taxon(split_line, taxa_levels, sample_name)
            kraken_report_taxa.append(taxon)
    # print(kraken_report_taxa[-1].percent_reads_assigned)
    return kraken_report_taxa

def add_parents_to_taxa(kraken_report, taxa_levels):
    assert kraken_report[0].name == 'unclassified'
    assert kraken_report[1].name == 'root'
    ## parent dict will keep the "current" taxon for each taxonomic level
    parent_dict = {}
    ## since unclassified doesn't have a parent ot children, not going to include it
    parent_dict[0] = kraken_report[0]
    ## setting root up as has no parent, but want it to be in the parent
    ## dict for reference by it's child/children
    parent_dict[1] = kraken_report[1]
    ## we need to keep track of when we go "up" the levels i.e. 
    ## from s. bongori to escherichia, which we do by comparing
    ## current taxonomic level to previous
    previous_taxonomic_level = 0
    for taxon in kraken_report[2:]:
        ## if previous taxonomic level is higher, that means we have moved from e.g. 
        ## A. ursingii (level 12) to Betaproteobacteria (level 7). Therefore, we 
        ## need to clean up everything in the parent dict between those levels
        ## the +1 is becayse python ranges are half open
        if previous_taxonomic_level >= taxon.taxonomic_level:
            to_del = range(taxon.taxonomic_level, previous_taxonomic_level + 1)
            for each in to_del:
                if each in parent_dict:
                    del(parent_dict[each])
        ## have to do it like this because levels can be skipped
        ## i.e. sometimes go from 8 to 11
        ## if the level higher is in the parent dict, that's the parent
        # print(vars(taxon))
        try:
            taxon.parent = parent_dict[taxon.taxonomic_level - 1]
        except KeyError:
            # print('KeyError')
            ## if it isn't (becayse might have been cleaned up by above)
            ## then take the highest level in the parent dict as parent
            taxon.parent = parent_dict[max(parent_dict.keys())]
        ## set the current taxon to it's level in the parent dict
        parent_dict[taxon.taxonomic_level] = taxon
        ## as the last thing set the current taxon as the "previous level"
        ## for the next loop
        previous_taxonomic_level = taxon.taxonomic_level
        # if hasattr(taxon, "parent"):
            # print(taxon.name, taxon.parent, sep = '\t')
    return kraken_report

def make_tree(kraken_report, print_tree):
    kraken_report[1].node = Node('root', taxon = kraken_report[1])
    for taxon in kraken_report[2:]:
        ## make the parent the node attached to the parent in the taxon class
        taxon.node = Node(taxon.name, parent = taxon.parent.node, taxon = taxon)
    # print_tree = False
    # print(print_tree)
    if print_tree is True:
        print(RenderTree(kraken_report[1].node))
    # print(kraken_report[1].node.name)
    return kraken_report[1].node

def parse_tree(kraken_tree, ranks_to_include, percent_reads_assigned_threshold, number_of_levels):
    '''
    1. find all nodes without children (i.e. tips)
    2. take path between each tip and root
    3. go up the path towards the root until get to 
    '''
    w = Walker()
    # print(kraken_tree)
    for node in PreOrderIter(kraken_tree):
        # print(dir(node))
        if node.is_leaf:
            # print(node)
            # print()
            i = 0
            ## only want two levels up from each tip
            while i <= number_of_levels:
                ## walk between the leaf node and the root
                ## output of walk is a tuple of tuples, hence the [0]
                for node2 in w.walk(node, kraken_tree.root)[0]:
                    ## only want to print species or genus level
                    if node2.taxon.rank in ranks_to_include:
                        ## if more than 0.05 reads assigned
                        if node2.taxon.percent_reads_assigned >= percent_reads_assigned_threshold:
                            ## prints double for genus as multiple tips lead to same genus
                            if node2.taxon.printed_already == False:
                                node2.taxon.print_info()
                                node2.taxon.printed_already = True
                    i += 1

def get_args():
    description = '''
    This script will read a kraken report, assign each taxon a parent based on it's
    position in the file and it's taxonomic level, and then construct a tree based on
    those relationships using AnyTree, which is then parsed to report only the two
    "bottom" levels from each tip which are species or genera and which have more than
    0.05% of reads assigned. These cutoffs are customisable (see help).
    '''
    parser = argparse.ArgumentParser(prog = 'parse_kraken2_report', description=description, add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', dest = 'inhandle', type = str, required = True, help = 'Path to kraken report file')
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", help="show this help message and exit")
    optional.add_argument('-l', dest = 'number_of_levels', type = int, default = 2, help = 'How far up from each tip do you want to check? If not working as expected, you may ned to alter -r as well.')
    optional.add_argument('-p', dest = 'percent_reads_assigned_threshold', type = float, default = 0.05, help = 'Minimum threshold of percent_reads_assigned for reporting')
    optional.add_argument('-r', dest = 'taxonomic_ranks', type = str, default = 'S,G', help = 'Taxonomic ranks which you want to report given in comma-separated, upper-case format, no spaces. Rank codes should reflect Kraken2 output documented here https://github.com/DerrickWood/kraken2/wiki/Manual#sample-report-output-format. Don\'t include number indicating sub-ranks. If not working as expected, you may need to alter -l as well.')
    optional.add_argument('-t', dest = 'print_tree', action = 'store_true', help = 'Include this option if you want to print the tree')

    args = parser.parse_args()
    args.taxonomic_ranks = args.taxonomic_ranks.split(',')
    return args

def check_args_print_tree(args_print_tree):
    ## separate function to allow testing
    assert args_print_tree in (True, False)

def check_args_taxonomic_ranks(args_taxonomic_ranks):
    valid_taxa_levels = ['U', 'R', 'D', 'K', 'P', 'C', 'O', 'F', 'G', 'S']
    assert len(set(args_taxonomic_ranks).intersection(valid_taxa_levels)) == len(args_taxonomic_ranks), f'The argument passed to taxonomic_ranks includes invalid options. Valid options are {valid_taxa_levels}'

def check_args_inhandle(args_inhandle):
    assert os.path.exists(args_inhandle)

def check_args(args):
    check_args_print_tree(args.print_tree)
    check_args_inhandle(args.inhandle)
    check_args_taxonomic_ranks(args.taxonomic_ranks)
    

def main(taxa_levels):
    '''
    0. read in kraken report
    1. go thorugh the report lines
    2. if the line has more than 0.05% of the reads, consider it for inclusion 
    in the output
    3. only include it in the output if there isn't an entry below it in the 
    taxonomic level which 
    '''
    args = get_args()
    check_args(args)
    kraken_report = read_kraken_report(args.inhandle, taxa_levels)
    kraken_report = add_parents_to_taxa(kraken_report, taxa_levels)
    kraken_tree = make_tree(kraken_report, args.print_tree)
    parse_tree(kraken_tree, args.taxonomic_ranks, args.percent_reads_assigned_threshold, args.number_of_levels)

# 
## probably going to need to replace this with getting the taxa levels from the 
## actual kraken results file.
taxa_levels = ['U', 'R', 'R1', 'D', 'D1', 'K', 'P', 'C', 'O', 'F', 'G', 'G1', 'S']



if __name__ == '__main__':
    main(taxa_levels)