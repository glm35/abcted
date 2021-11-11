import unittest


from abcted.abc2midi import get_midi_note


class TestGetMidiNote(unittest.TestCase):
    def test_c3(self):
        midi_note = get_midi_note("C,")
        self.assertEqual(48, midi_note)

    def test_c4(self):
        midi_note = get_midi_note('C')
        self.assertEqual(60, midi_note)

    def test_c5(self):
        midi_note = get_midi_note('c')
        self.assertEqual(72, midi_note)

    def test_c6(self):
        midi_note = get_midi_note("c'")
        self.assertEqual(84, midi_note)

    def test_c4_sharp(self):
        midi_note = get_midi_note('^C')
        self.assertEqual(61, midi_note)

    def test_c4_double_sharp(self):
        midi_note = get_midi_note('^^C')
        self.assertEqual(62, midi_note)

    def test_e4(self):
        midi_note = get_midi_note('E')
        self.assertEqual(64, midi_note)

    def test_e4_flat(self):
        midi_note = get_midi_note('_E')
        self.assertEqual(63, midi_note)

    def test_e4_double_flat(self):
        midi_note = get_midi_note('__E')
        self.assertEqual(62, midi_note)


if __name__ == '__main__':
    unittest.main()
