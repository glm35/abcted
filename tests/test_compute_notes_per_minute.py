import unittest


import abcde.abcparser as abcparser
from abcde.abc2seq import compute_notes_per_minute, AbcSequencerException


class TestComputeNotesPerMinute(unittest.TestCase):
    @staticmethod
    def _parse_input(default_note_length_header, meter_header,
                     tempo_header):
        default_note_length = None
        meter = None
        tempo = None

        if default_note_length_header is not None:
            default_note_length = \
                abcparser.parse_default_note_length(default_note_length_header)
        if meter_header is not None:
            meter = abcparser.parse_meter(meter_header)
        if tempo_header is not None:
            tempo = abcparser.parse_tempo(tempo_header)

        return default_note_length, meter, tempo

    def test_simple(self):
        default_note_length_header = None
        meter_header = '4/4'
        tempo_header = '60'

        (default_note_length, meter, tempo) = self._parse_input(
            default_note_length_header, meter_header, tempo_header)

        npm = compute_notes_per_minute(default_note_length, meter, tempo)
        self.assertEqual(60, npm)

    def test_slow_reel(self):
        default_note_length_header = '1/8'
        meter_header = '2/2'
        tempo_header = '1/2=80'

        (default_note_length, meter, tempo) = self._parse_input(
            default_note_length_header, meter_header, tempo_header)

        npm = compute_notes_per_minute(default_note_length, meter, tempo)
        self.assertEqual(320, npm)

    def test_jig(self):
        default_note_length_header = '1/8'
        meter_header = '6/8'
        tempo_header = '3/8=120'

        (default_note_length, meter, tempo) = self._parse_input(
            default_note_length_header, meter_header, tempo_header)

        npm = compute_notes_per_minute(default_note_length, meter, tempo)
        self.assertEqual(360, npm)

    def test_error_missing_meter(self):
        tempo_header = '60'
        tempo = abcparser.parse_tempo(tempo_header)

        self.assertRaises(AbcSequencerException,
                          compute_notes_per_minute, None, None, tempo)

    def test_error_missing_tempo(self):
        meter_header = '4/4'
        meter = abcparser.parse_meter(meter_header)

        self.assertRaises(AbcSequencerException,
                          compute_notes_per_minute, None, meter, None)


if __name__ == '__main__':
    unittest.main()
