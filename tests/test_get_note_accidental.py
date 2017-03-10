import unittest


from abcde.abcparser import get_accidental


class TestGetNoteAccidental(unittest.TestCase):

    # Nominal test cases

    def test_natural(self):
        accidental = get_accidental(cur_line_to_insert='=')
        self.assertEqual('=', accidental)

    def test_sharp(self):
        accidental = get_accidental(cur_line_to_insert='^')
        self.assertEqual('^', accidental)

    def test_double_sharp(self):
        accidental = get_accidental(cur_line_to_insert='^^')
        self.assertEqual('^^', accidental)

    def test_flat(self):
        accidental = get_accidental(cur_line_to_insert='_')
        self.assertEqual('_', accidental)

    def test_double_flat(self):
        accidental = get_accidental(cur_line_to_insert='__')
        self.assertEqual('__', accidental)

    # Special test cases

    def test_empty_line(self):
        accidental = get_accidental(cur_line_to_insert='')
        self.assertEqual('', accidental)

    def test_invalid_mixed_accidentals(self):
        accidental = get_accidental(cur_line_to_insert='^_')
        self.assertEqual('_', accidental)

    def test_more_data_in_line(self):
        accidental = get_accidental(cur_line_to_insert='CDEF GABc | CDEF GAB^')
        self.assertEqual('^', accidental)


if __name__ == '__main__':
    unittest.main()
