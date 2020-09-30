import unittest


from kraken2_scripts.parse_kraken2_report import Taxon, taxa_levels


class TestParseKraken2Report(unittest.TestCase):
    def test_taxon_class_init(self):
        ## salmonella rank is not actually S1, it's just S, but added the S1 to test the rank/full rank switch
        split_line = ['26.78', '759833', '759833', 'S1', '28901', '                Salmonella enterica']
        taxa = Taxon(split_line)
        self.assertEqual(taxa.percent_reads_assigned, 26.78, 'Taxon class did not read in percent_reads_assigned correctly') 
        self.assertEqual(taxa.number_reads_rooted_here, 759833, 'Taxon class did not read in number_reads_rooted_here correctly')
        self.assertEqual(taxa.number_reads_assigned_here, 759833, 'Taxon class did not read in number_reads_assigned_here correctly')
        self.assertEqual(taxa.full_rank, 'S1', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.rank, 'S', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.ncbi_id, 28901, 'Taxon class did not read in ncbi_id correctly')
        self.assertEqual(taxa.name, 'Salmonella enterica', 'Taxon class did not read in name correctly')

    def test_taxa_levels(self):
        self.assertEqual(taxa_levels, ['U', 'R', 'D', 'K', 'P', 'C', 'O', 'F', 'G', 'S'], 'Taxa levels corrupted')


if __name__ == '__main__':
    unittest.main()