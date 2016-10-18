import unittest


from abcde.abc2midi import get_mode_alteration


class TestGetModeAlteration(unittest.TestCase):
    def test_c_in_cmaj(self):
        alteration = get_mode_alteration('C', 'Cmaj')
        self.assertEqual(0, alteration)

    def test_f_in_gmaj(self):
        alteration = get_mode_alteration('F', 'Gmaj')
        self.assertEqual(1, alteration)


if __name__ == '__main__':
    unittest.main()
