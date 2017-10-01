import unittest


from abcde.abcparser import normalize_abc_key, AbcParserException


class TestNormalizeAbcKey(unittest.TestCase):
    def test_cmaj(self):
        (base_note, mode) = normalize_abc_key('Cmajor')
        self.assertEqual('C', base_note)
        self.assertEqual('maj', mode)

    def test_dmix(self):
        (base_note, mode) = normalize_abc_key('Dmixolydian')
        self.assertEqual('D', base_note)
        self.assertEqual('mix', mode)

    def test_ador(self):
        (base_note, mode) = normalize_abc_key('Adorian')
        self.assertEqual('A', base_note)
        self.assertEqual('dor', mode)

    def test_eeol(self):
        (base_note, mode) = normalize_abc_key('Eeolian')
        self.assertEqual('E', base_note)
        self.assertEqual('min', mode)

    def test_f_sharp_maj(self):
        (base_note, mode) = normalize_abc_key('F#maj')
        self.assertEqual('F#', base_note)
        self.assertEqual('maj', mode)

    def test_b_flat_maj(self):
        (base_note, mode) = normalize_abc_key('Bbmaj')
        self.assertEqual('Bb', base_note)
        self.assertEqual('maj', mode)

    # Test input sanitization
    def test_g_with_leading_and_trailing_spaces(self):
        (base_note, mode) = normalize_abc_key(' G  ')
        self.assertEqual('G', base_note)
        self.assertEqual('maj', mode)

    # Test exceptions
    def test_invalid_key_a_sharp_maj(self):
        self.assertRaises(AbcParserException, normalize_abc_key, 'A#')

    def test_invalid_key_b_schtroumpf(self):
        self.assertRaises(AbcParserException, normalize_abc_key, 'Bschtroumpf')

if __name__ == '__main__':
    unittest.main()
