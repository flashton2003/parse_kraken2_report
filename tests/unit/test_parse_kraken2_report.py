import unittest


from kraken2_scripts.parse_kraken2_report import Taxon, taxa_levels


class TestParseKraken2Report(unittest.TestCase):


    def test_taxon_class_init(self):
        ## salmonella rank is not actually S1, it's just S, but added the S1 to test the rank/full rank switch
        split_line = ['26.78', '759833', '759833', 'G1', '28901', '                Salmonella']
        sample_name = '18080-1-FR10242277'
        taxa = Taxon(split_line, taxa_levels, sample_name)
        self.assertEqual(taxa.percent_reads_assigned, 26.78, 'Taxon class did not read in percent_reads_assigned correctly') 
        self.assertEqual(taxa.number_reads_rooted_here, 759833, 'Taxon class did not read in number_reads_rooted_here correctly')
        self.assertEqual(taxa.number_reads_assigned_here, 759833, 'Taxon class did not read in number_reads_assigned_here correctly')
        self.assertEqual(taxa.full_rank, 'G1', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.rank, 'G', 'Taxon class did not read in rank correctly')
        self.assertEqual(taxa.ncbi_id, 28901, 'Taxon class did not read in ncbi_id correctly')
        self.assertEqual(taxa.name, 'Salmonella', 'Taxon class did not read in name correctly')
        self.assertEqual(taxa.printed_already, False, 'Taxon class printed_already not False')

    def test_taxa_levels(self):
        self.assertEqual(taxa_levels, ['U', 'R', 'R1', 'D', 'D1', 'K', 'P', 'C', 'O', 'F', 'G', 'G1', 'S'], 'Taxa levels corrupted')


if __name__ == '__main__':
    unittest.main()