import unittest


from abcde.musictheory import get_note_alteration_in_key


class TestGetNoteAlterationInKey(unittest.TestCase):
    def test_c_in_cmaj(self):
        alteration = get_note_alteration_in_key('C', ('C', 'maj'))
        self.assertEqual('', alteration)

    # Test major scales with sharp notes

    def test_f_in_gmaj(self):
        alteration = get_note_alteration_in_key('F', ('G', 'maj'))
        self.assertEqual('^', alteration)

    def test_c_in_dmaj(self):
        alteration = get_note_alteration_in_key('C', ('D', 'maj'))
        self.assertEqual('^', alteration)

    def test_e_in_dmaj(self):
        alteration = get_note_alteration_in_key('E', ('D', 'maj'))
        self.assertEqual('', alteration)

    def test_b_in_c_sharp_maj(self):
        alteration = get_note_alteration_in_key('B', ('C#', 'maj'))
        self.assertEqual('^', alteration)

    # Test major scales with flat notes

    def test_b_in_fmaj(self):
        alteration = get_note_alteration_in_key('B', ('F', 'maj'))
        self.assertEqual('_', alteration)

    def test_e_in_b_flat_maj(self):
        alteration = get_note_alteration_in_key('E', ('Bb', 'maj'))
        self.assertEqual('_', alteration)

    # Test modes

    def test_c_in_dmix(self):
        alteration = get_note_alteration_in_key('C', ('D', 'mix'))
        self.assertEqual('', alteration)

    def test_f_in_dmix(self):
        alteration = get_note_alteration_in_key('F', ('D', 'mix'))
        self.assertEqual('^', alteration)

    def test_e_in_cmin(self):
        alteration = get_note_alteration_in_key('E', ('C', 'min'))
        self.assertEqual('_', alteration)

    def test_e_in_cdor(self):
        alteration = get_note_alteration_in_key('E', ('C', 'dor'))
        self.assertEqual('_', alteration)

    def test_b_in_cdor(self):
        alteration = get_note_alteration_in_key('B', ('C', 'dor'))
        self.assertEqual('_', alteration)

    def test_f_in_c_sharp_lyd(self):
        alteration = get_note_alteration_in_key('F', ('C#', 'lyd'))
        self.assertEqual('^^', alteration)

    def test_e_in_d_flat_phr(self):
        alteration = get_note_alteration_in_key('E', ('Db', 'phr'))
        self.assertEqual('__', alteration)


if __name__ == '__main__':
    unittest.main()
