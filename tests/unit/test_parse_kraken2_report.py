import unittest


from kraken2_scripts.parse_kraken2_report import my_sum, read_kraken_report

class TestSum(unittest.TestCase):
    def test_list_int(self):
        '''
        Test that it can sum a list of integers
        '''
        data = [1, 2, 3]
        result = my_sum(data)
        self.assertEqual(result, 6)

class TestTaxonClassInit(unittest.TestCase):
    def test_taxon_class_init(self):
        split_line = 

if __name__ == '__main__':
    unittest.main()