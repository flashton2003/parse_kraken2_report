import os
import string
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
    sample_name = inhandle.split('/')[-1].split('.')[0]
    kraken_report_taxa = []
    with open(inhandle) as fi:
        for line in fi.readlines():
            split_line = line.strip().split('\t')
            # print(split_line)
            taxon = Taxon(split_line, taxa_levels, sample_name)
            kraken_report_taxa.append(taxon)
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

def make_tree(kraken_report):
    kraken_report[1].node = Node('root', taxon = kraken_report[1])
    for taxon in kraken_report[2:]:
        ## make the parent the node attached to the parent in the taxon class
        taxon.node = Node(taxon.name, parent = taxon.parent.node, taxon = taxon)
    return kraken_report[1].node
    # print(RenderTree(kraken_report[1].node))

def parse_tree(kraken_tree):
    '''
    1. find all nodes without children (i.e. tips)
    2. take path between each tip and root
    3. go up the path towards the root until get to 
    '''
    w = Walker()
    # print(kraken_tree.root)
    for node in PreOrderIter(kraken_tree):
        # print(dir(node))
        if node.is_leaf:
            # print(node)
            # print()
            i = 0
            ## only want two levels up from each tip
            while i < 3:
                ## walk between the leaf node and the root
                ## output of walk is a tuple of tuples, hence the [0]
                for node2 in w.walk(node, kraken_tree.root)[0]:
                    ## only want to print species or genus level
                    if node2.taxon.rank in ('S', 'G'):
                        ## if more than 0.05 reads assigned
                        if node2.taxon.percent_reads_assigned >= 0.05:
                            ## prints double for genus as multiple tips lead to same genus
                            if node2.taxon.printed_already == False:
                                node2.taxon.print_info()
                                node2.taxon.printed_already = True
                    i += 1
                # if node2.taxon

    # pass

def main(inhandle, taxa_levels):
    '''
    0. read in kraken report
    1. go thorugh the report lines
    2. if the line has more than 0.05% of the reads, consider it for inclusion in the output
    3. only include it in the output if there isn't an entry below it in the taxonomic level which 
    '''
    kraken_report_taxa = read_kraken_report(inhandle, taxa_levels)
    kraken_report = add_parents_to_taxa(kraken_report_taxa, taxa_levels)
    kraken_tree = make_tree(kraken_report)
    parse_tree(kraken_tree)
    # parse_report(kraken_report)

inhandle = '/Users/flashton/Dropbox/GordonGroup/ben_kumwenda_genomes/kraken2/results/2020.09.30/18080-1-FR10242277.kraken_report.txt'
## probably going to need to replace this with getting the taxa levels from the 
## actual kraken results file.
taxa_levels = ['U', 'R', 'R1', 'D', 'D1', 'K', 'P', 'C', 'O', 'F', 'G', 'G1', 'S']

assert os.path.exists(inhandle)

if __name__ == '__main__':
    main(inhandle, taxa_levels)