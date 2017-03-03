import unittest


from abcde.abcparser import normalize_abc_key


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


if __name__ == '__main__':
    unittest.main()
