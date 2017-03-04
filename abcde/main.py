#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.font
import tkinter.scrolledtext

import abcparser
import abc2midi
import musictheory
import snap


class Theme():
    def __init__(self, theme = 'TedPy'):
        # The 'TedPy' theme:
        self.bg = '#222222'     # Background color
        self.fg = 'white'       # Foreground color
        self.insertbg = 'white' # Insertion cursor color
        self.selectbg = '#630'  # Select background color

        self.font_family = "courier new"
        self.font_size = 12

    def get_font(self):
        return tkinter.font.Font(family=self.font_family, size=self.font_size)


def maximize_root_window(root):
    """Maximize the root window"""
    root_w, root_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (root_w, root_h))


class EditZone(tkinter.Frame):
    def __init__(self, frame, theme):
        self.theme = theme
        self.edit_zone = tkinter.scrolledtext.ScrolledText(
            frame, font=theme.get_font(),
            background=theme.bg, foreground=theme.fg,

            # Cursor configuration:
            insertbackground=theme.insertbg,
            #insertofftime=0, # Disable blinking
            #insertwidth=8, # Cursor width

            # Selection configuration:
            selectbackground=theme.selectbg)

        self.shift = False
        self.control = False
        self.alt = False

        self.edit_zone.focus() # Set the focus on the edit zone

        self.edit_zone.bind('<Key>', self.on_key_press)
        self.edit_zone.bind('<KeyRelease>', self.on_key_release)

        self.edit_zone.pack(expand=tkinter.YES, fill=tkinter.BOTH)

        self.snap = snap.SingleNoteAbcPlayer()
        self.snap.midi_channel = 1
        self.snap.select_instrument('Acoustic Grand Piano')

    def on_key_press(self, event):
        #print("key pressed: " + event.keysym)
        if event.keysym in ['Shift_R','Shift_L']:
            self.shift = True
        elif event.keysym in ['Control_L','Control_R']:
            self.control = True
        elif event.keysym in ['Alt_L']:
            self.alt = True
        elif not self.control and not self.alt and \
                        event.keysym.upper() in musictheory.c_major_scale:
            abc_note = self.get_note_to_play(event.keysym)
            if abc_note is not None:
                self.snap.play_midi_note(abc2midi.get_midi_note(abc_note))

        elif event.keysym in ['t']: # Test!
            self.get_cur_line_to_insert()
#            print("Current cursor position: " + self.edit_zone.index(tkinter.INSERT))
#
#            print(self.edit_zone.get('1.0'))
#            print(self.edit_zone.get(tkinter.INSERT))
#            print(self.edit_zone.get('1.0', tkinter.END))

    def on_key_release(self, event):
        if event.keysym in ['Shift_R','Shift_L']:
            self.shift = False
        elif event.keysym in ['Control_L','Control_R']:
            self.control = False
        elif event.keysym in ['Alt_L']:
            self.alt = False

    def get_cur_line_to_insert(self):
        """Get the current line of text from the beginning of the line to the
        insertion point (text cursor).

        :return: a string
        """
        insert_index = self.edit_zone.index(tkinter.INSERT)
        (cur_line, cur_col) = insert_index.split('.')
        line_start_index = '{}.{}'.format(cur_line, 0)
        cur_line_to_insert = self.edit_zone.get(line_start_index, insert_index)
        return cur_line_to_insert

    def get_line(self, line_no):
        index_start = str(line_no) + ".0"
        index_end = str(line_no) + ".end"
        return self.edit_zone.get(index_start, index_end)

    def get_key_at_insert(self):
        """Get the tune key at the insertion point (text cursor).

        :return: a string with the tune key, eg 'C' or 'Eb minor' or 'A mix'
        """

        # Assume 'C major' if no key is specified
        key = 'C'

        # For each line going upward until until the line starts with 'X:'
        # (beginning of the tune found) or until there are no more lines,
        # look for the key:

        line_no = int(self.edit_zone.index(tkinter.INSERT).split('.')[0])
        while line_no > 0:
            line = self.get_line(line_no)
            if line.startswith('K:'):
                key = line[2:]
                break
            if line.startswith('X:'):
                # We reached the beginning of the tune
                break
            line_no -= 1

        return key

    def get_note_to_play(self, keysym):
        """Given a keysym following a key press, check whether there is a
         note to play. If so, return the note.

         :param keysym The key pressed. It has to be a valid ABC note, ie its
                       lower-case value must belong to musictheory.c_major_scale

         :return a String with the note to play in ABC-normalized format, or None
                 if there is no note to play. The note is absolute, ie not relative to
                 the tune scale. Examples: 'c', "c'", 'C', 'C,,', '^C' (C sharp), '_c' (c flat)
         """

        assert 'a' <= keysym <= 'g' or 'A' <= keysym <= 'G'
        abc_note = keysym

        # Check whether we are in comment context
        cur_line_to_insert = self.get_cur_line_to_insert()
        if cur_line_to_insert.find('%') != -1:
            # There is a '%' before the text cursor => we are in comment context
            return None

        # Check whether we are in an information line
        if len(cur_line_to_insert) >= 2:
            if cur_line_to_insert[1] is ':':
                if 'A' <= cur_line_to_insert[0] <= 'Z':
                    return  None

        # Find the tune key at the insertion point
        key = self.get_key_at_insert()
        print("Key at insert: " + key)
        abc_key = abcparser.normalize_abc_key(key)

        # Find whether there is an accidental before the note

        # Get the note to play with all the useful attributes (accidentals,
        # octave changes, ...)
        alteration = musictheory.get_note_alteration_in_key(abc_note, abc_key)
        abc_note = alteration + abc_note

        return abc_note


def main():
    root = tkinter.Tk()
    root.title("abcde")
    #maximize_root_window(root)

    theme = Theme()
    edit_zone = EditZone(root, theme)

    root.mainloop()


if __name__ == "__main__":
    main()
