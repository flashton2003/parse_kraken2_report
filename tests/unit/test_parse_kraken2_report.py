import unittest
import os

from kraken2_scripts.parse_kraken2_report import Taxon, all_taxa_levels, valid_taxa_levels, check_args_print_tree, check_args_taxonomic_ranks, check_args_inhandle, read_kraken_report


class TestParseKraken2Report(unittest.TestCase):
    
    def test_taxon_class_init(self):
        ## salmonella rank is not actually S1, it's just S, but added the S1 to test the rank/full rank switch
        split_line = ['26.78', '759833', '759833', 'G1', '28901', '                Salmonella']
        sample_name = '18080-1-FR10242277'
        taxa = Taxon(split_line, all_taxa_levels, sample_name)
        self.assertEqual(taxa.percent_reads_assigned, 26.78, 'Taxon class did not read in percent_reads_assigned correctly') 
        self.assertEqual(taxa.number_reads_rooted_here, 759833, 'Taxon class did not read in number_reads_rooted_here correctly')
        self.assertEqual(taxa.number_reads_assigned_here, 759833, 'Taxon class did not read in number_reads_assigned_here correctly')
        self.assertEqual(taxa.full_rank, 'G1', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.rank, 'G', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.ncbi_id, 28901, 'Taxon class did not read in ncbi_id correctly')
        self.assertEqual(taxa.name, 'Salmonella', 'Taxon class did not read in name correctly')
        self.assertEqual(taxa.printed_already, False, 'Taxon class printed_already not False')

    def test_taxa_levels(self):
        self.assertEqual(all_taxa_levels, ['U', 'R', 'R1', 'D', 'D1', 'D2', 'D3', 'K', 'P', 'P1', 'P2', 'C', 'C1', 'C2', 'O', 'O1', 'O2', 'F', 'F1', 'F2', 'G', 'G1', 'S', 'S1'], 'Taxa levels dont match reference')

    def test_check_args(self):
        # args = argparse.ArgumentParser()
        # parser.add_args(dest = 'print_tree')
        check_args_print_tree(True)
        check_args_print_tree(False)
        with self.assertRaises(AssertionError):
            check_args_print_tree('False')
            check_args_print_tree(123)

    def test_check_args_taxonomic_ranks(self):
        check_args_taxonomic_ranks(['S', 'G'], valid_taxa_levels)
        with self.assertRaises(AssertionError):
            check_args_taxonomic_ranks(['S', 'G', 'T'], valid_taxa_levels)

    def test_check_args_inhandle(self):
        check_args_inhandle(os.path.abspath(__file__))
        with self.assertRaises(AssertionError):
            check_args_inhandle('blah_random_jbfjshbdfjsbfk')
        




if __name__ == '__main__':
    unittest.main()