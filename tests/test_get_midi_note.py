import unittest


from abcde.abc2midi import get_midi_note


class TestGetMidiNote(unittest.TestCase):
    def test_c4(self):
        midi_note = get_midi_note('C')
        self.assertEqual(60, midi_note)

    def test_e4(self):
        midi_note = get_midi_note('E')
        self.assertEqual(64, midi_note)


if __name__ == '__main__':
    unittest.main()
