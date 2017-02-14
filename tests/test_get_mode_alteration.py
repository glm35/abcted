import unittest


from abcde.abc2midi import get_mode_alteration


class TestGetModeAlteration(unittest.TestCase):
    def test_c_in_cmaj(self):
        alteration = get_mode_alteration('C', 'Cmaj')
        self.assertEqual(0, alteration)

    # Test major scales with sharp notes

    def test_f_in_gmaj(self):
        alteration = get_mode_alteration('F', 'Gmaj')
        self.assertEqual(1, alteration)

    def test_c_in_dmaj(self):
        alteration = get_mode_alteration('C', 'Dmaj')
        self.assertEqual(1, alteration)

    def test_e_in_dmaj(self):
        alteration = get_mode_alteration('E', 'Dmaj')
        self.assertEqual(0, alteration)

    def test_b_in_c_sharp_maj(self):
        alteration = get_mode_alteration('B', 'C#maj')
        self.assertEqual(1, alteration)

    # Test major scales with flat notes

    def test_b_in_fmaj(self):
        alteration = get_mode_alteration('B', 'Fmaj')
        self.assertEqual(-1, alteration)

    def test_e_in_b_flat_maj(self):
        alteration = get_mode_alteration('E', 'Bbmaj')
        self.assertEqual(-1, alteration)

    # Test modes

    def test_c_in_dmix(self):
        alteration = get_mode_alteration('C', 'Dmix')
        self.assertEqual(0, alteration)

    def test_f_in_dmix(self):
        alteration = get_mode_alteration('F', 'Dmix')
        self.assertEqual(1, alteration)


if __name__ == '__main__':
    unittest.main()
