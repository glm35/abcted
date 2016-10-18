import unittest


from abcde.abc2midi import get_midi_note


class TestGet_midi_note(unittest.TestCase):
    def test_c4(self):
        midi_note = get_midi_note('C')
        self.assertEqual(60, midi_note)

    def test_e4(self):
        midi_note = get_midi_note('E')
        self.assertEqual(64, midi_note)

    def test_f4_in_d_major(self):
        midi_note = get_midi_note('F', 'Dmaj')
        self.assertEqual(66, midi_note)


if __name__ == '__main__':
    unittest.main()
