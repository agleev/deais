import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
import src.values as values

class TestValuesMSG(unittest.TestCase):
    
    def test_get_lan_lot(self):
        self.assertEqual(values.get_lan_lot("0000100010110011111111000111"), 15.209718)
        self.assertEqual(values.get_lan_lot("010011100101110111011101000"), 68.477827)
        self.assertEqual(values.get_lan_lot("1111011100110001011001000111"), -15.391455)
        self.assertEqual(values.get_lan_lot("010110000110101111000110100"), 77.263447)
        
        
    def test_get_eta(self):
        self.assertEqual(values.get_eta('1000000000000000', 40), '00')
        self.assertEqual(values.get_eta('111011', 59), '59')
        self.assertEqual(values.get_eta('11111', 31), '31')
        self.assertEqual(values.get_eta('1100', 12), '12')
        self.assertEqual(values.get_eta('10111', 23), '23')
        self.assertEqual(values.get_eta('10111', 0), '00')

    def test_get_eta(self):
        self.assertEqual(values.get_string_field("010111001001001100001100001001000001001101100000001010001111011001000000000000"), 'WILLIAM JOY')
        self.assertEqual(values.get_string_field("010111001001001100001100001001000001001101100000001010001111011001000000000000101010"), 'WILLIAM JOY*')
        self.assertEqual(values.get_string_field("000000000000000000000000000000000000000000000000000000000000100001"), '!')
        
    def test_get_shiptype(self):
        self.assertEqual(values.get_shiptype('00000000'), 0)
        self.assertEqual(values.get_shiptype('01100111'), 0)
        self.assertEqual(values.get_shiptype('01100011'), 99)
if __name__ == '__main__':
    
    unittest.main(verbosity=2)