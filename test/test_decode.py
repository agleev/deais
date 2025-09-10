import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from src.message import get_vessel_name



class TestDecodeMSG(unittest.TestCase):
    
    def test_get_vessel_name(self):
        self.assertEqual(get_vessel_name("000010010101000111010011011001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"), "BUGSY")


if __name__ == '__main__':
    unittest.main(verbosity=2)