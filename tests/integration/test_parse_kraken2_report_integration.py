
import os
import io
import sys
import unittest
from kraken2_scripts.parse_kraken2_report import Taxon, taxa_levels, check_args_print_tree, check_args_taxonomic_ranks, check_args_inhandle, read_kraken_report, parse_tree, add_parents_to_taxa, make_tree

class TestParseKraken2Report(unittest.TestCase):
    
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.inhandle = os.path.join(dirname, 'fixtures', '18080-1-FR10242277.kraken_report.txt')
    
    def test_read_kraken_report(self):
        kraken_report = read_kraken_report(self.inhandle, taxa_levels)
        self.assertEqual(len(kraken_report), 51, 'kraken_report_taxa wrong length')
        self.assertEqual(kraken_report[0].name, 'unclassified', 'first entry in kraken_report_taxa wrong name')
        self.assertEqual(kraken_report[-1].name, 'Bacillus', 'first entry in kraken_report_taxa wrong name')
        self.assertEqual(kraken_report[-1].percent_reads_assigned, 0.0, 'percent_reads_assigned being read wrong')

    def test_add_parents_to_taxa(self):
        kraken_report = read_kraken_report(self.inhandle, taxa_levels)
        kraken_report = add_parents_to_taxa(kraken_report, taxa_levels)
        self.assertEqual(kraken_report[5].parent.name, 'Proteobacteria', 'Parent not beingn assigned correctly')
        self.assertEqual(kraken_report[25].parent.name, 'Acinetobacter', 'Parent not beingn assigned correctly')

    def test_make_tree(self):
        kraken_report = read_kraken_report(self.inhandle, taxa_levels)
        kraken_report = add_parents_to_taxa(kraken_report, taxa_levels)
        kraken_tree = make_tree(kraken_report, False)
        self.assertEqual(kraken_tree.name, 'root', 'check tree construction')

    def test_parse_tree(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        kraken_report = read_kraken_report(self.inhandle, taxa_levels)
        kraken_report = add_parents_to_taxa(kraken_report, taxa_levels)
        kraken_tree = make_tree(kraken_report, False)
        parse_tree(kraken_tree, ['S', 'G'], 0.05, 2)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().split('\n')
        self.assertEqual(len(output), 5, '5 lines (4 results and new line) arent printed with defaults') 
        self.assertEqual(output[-2].split('\t')[-1], 'Escherichia', 'Check printed output') 