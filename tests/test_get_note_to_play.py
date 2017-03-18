import unittest


from abcde.abcparser import get_note_to_play
import ui.edit_zone


class MockEditZone(ui.edit_zone.EditZone):
    """Behave like an EditZone object, operating on a simple array of lines,
    where the cursor is at the end of the last line
    """

    def __init__(self, raw_abc):
        self.raw_abc = raw_abc
        self.abc_lines = raw_abc.split('\n')

    def get_current_line_to_cursor(self):
        return self.abc_lines[-1]

    def get_line(self, line_no):
        return self.abc_lines[line_no - 1]

    def get_line_no_at_cursor(self):
        return len(self.abc_lines)


class TestGetNoteToPlay(unittest.TestCase):
    def test_c_in_c(self):
        raw_abc = """K:C\nCDEF GAB"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='c')
        self.assertEqual('c', note_to_play)

    def test_f_in_g(self):
        raw_abc = """K:G\nCDEF GAB"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='f')
        self.assertEqual('^f', note_to_play)

    def test_f_natural_in_g(self):
        raw_abc = """K:G\nCDEF GAB="""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='f')
        self.assertEqual('f', note_to_play)

    # Test octave markers

    def test_upper_c_in_c(self):
        raw_abc = """K:C\nCDEF GABc"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym="'")
        self.assertEqual("c'", note_to_play)

    def test_lower_c_in_c(self):
        raw_abc = """K:C\nC"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym=',')
        self.assertEqual("C,", note_to_play)

    def test_no_note_before_octave_marker(self):
        raw_abc = """K:C\nCDEF GABc z"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym="'")
        self.assertEqual(None, note_to_play)

    def test_nothing_before_octave_marker(self):
        raw_abc = """K:C\n"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym="'")
        self.assertEqual(None, note_to_play)

    def test_absolutely_nothing_before_octave_marker(self):
        raw_abc = ''
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym="'")
        self.assertEqual(None, note_to_play)

    def test_error_comma_after_upper_case_note(self):
        raw_abc = """K:C\nCDEF GABc"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym=',')
        self.assertEqual(None, note_to_play)

    def test_error_apostrophe_after_lower_case_note(self):
        raw_abc = """K:C\nCDEF GABC"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym="'")
        self.assertEqual(None, note_to_play)

    # Special cases

    def test_not_a_note(self):
        raw_abc = """K:G\nCDEF GAB"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='t')
        self.assertEqual(None, note_to_play)

    def test_in_comment(self):
        raw_abc = """K:G\n% CDEF GAB"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='c')
        self.assertEqual(None, note_to_play)

    def test_in_info_field(self):
        raw_abc = """K:G\nC:Paddy F"""
        mock_edit_zone = MockEditZone(raw_abc)
        note_to_play = get_note_to_play(mock_edit_zone, keysym='a')
        self.assertEqual(None, note_to_play)


if __name__ == '__main__':
    unittest.main()
