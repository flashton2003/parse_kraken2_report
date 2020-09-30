import unittest


from kraken2_scripts.parse_kraken2_report import my_sum

class TestSum(unittest.TestCase):
    def test_list_int(self):
        '''
        Test that it can sum a list of integers
        '''
        data = [1, 2, 3]
        result = my_sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()