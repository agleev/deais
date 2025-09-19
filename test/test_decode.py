import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
import src.decode as decode



class TestDecodeMSG(unittest.TestCase):
    
    def test_bit_shifts(self):
        self.assertEqual(decode.bit_shifts(43,2),'1010')
        self.assertEqual(decode.bit_shifts(23,3), '010')

    def test_ascii_8b_to_6b(self):
        self.assertEqual(decode.ascii_8b_to_6b(48), 0)
        self.assertEqual(decode.ascii_8b_to_6b(57), 9)
        
    def test_decode_msg(self):
        self.assertEqual(decode.decode_msg(b"139tH:4v@0KmGgtbOq=UKlGd88PDC4h"),
        '000001000011001001111100011000001010000100111110010000000000011011110101010111101111111100101010011111111001001101100101011011110100010111101100001000001000100000010100010011000100110000')

    def test_bin_to_signed(self):
        self.assertEqual(decode.bin_to_signed("1010110011110101101101001011"), -87073973)
        self.assertEqual(decode.bin_to_signed("0010110011110101101101001011"), 47143755)
    
    def test_proc_6bit_cha(self):
        self.assertEqual(decode.proc_6bit_cha("010111001001001100001100001001000001001101100000001010001111011001000000000000"), "WILLIAM JOY@@")
        self.assertEqual(decode.proc_6bit_cha("110101110000100000001100000101010100100000010000001111000010000101000100011001"), "50 LET POBEDY")
        self.assertEqual(decode.proc_6bit_cha("001011001101100000010011000101000111000001010010000001100000010100010101001110000001"), "KM SEGARA TUNA")
    
    def test_get_ascii(self):
        self.assertEqual(decode.get_ascii("1000000"),"@")
        self.assertEqual(decode.get_ascii("000000"),"@")
        self.assertEqual(decode.get_ascii("000010"),"B")
        self.assertEqual(decode.get_ascii("100001100001100001"),"!")
    
if __name__ == '__main__':
    unittest.main(verbosity=2)