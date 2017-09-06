import unittest

from emmail.objects.clusterer import Clusterer
from emmail.tests.test_data import *

# Single BLAST output file

clusterer = Clusterer(blastOutputFile=test_blast_product, 
                        output_stream="stdout",
                        verbose=False,
                        binwidth=800)

clusterer_verbose = Clusterer(blastOutputFile=test_blast_product, 
                        output_stream="stdout",
                        verbose=True,
                        binwidth=800)                        
                        
class testClusterer(unittest.TestCase):

    def test_null(self):
        self.assertEqual(test_null, "this is a null test")

    def test_is_clusterer(self):
        self.assertIs(type(clusterer), Clusterer)
        self.assertIs(type(clusterer_verbose), Clusterer)
        
    def test_run_short(self):
        self.assertEqual(clusterer.main(), clusterer_result_short)
        
    def test_run_verbose(self):
        self.assertEqual(clusterer_verbose.main(), clusterer_result_verbose)
        
if __name__ == "__main__":
    unittest.main()