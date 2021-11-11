import unittest


import abcted.abc2seq as abc2seq


class TestComputeTicksPerNote(unittest.TestCase):
    def test_simple(self):
        notes_per_minute = 60
        tpn = abc2seq.compute_ticks_per_note(notes_per_minute)
        self.assertEqual(480, tpn)

    def test_slow_reel(self):
        notes_per_minute = 320
        tpn = abc2seq.compute_ticks_per_note(notes_per_minute)
        self.assertEqual(120, tpn)

    def test_jig(self):
        notes_per_minute = 360
        tpn = abc2seq.compute_ticks_per_note(notes_per_minute)
        self.assertEqual(120, tpn)


if __name__ == '__main__':
    unittest.main()
