#!/usr/bin/env python3

import io
import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from pico8 import util


class TestUtil(unittest.TestCase):
    def setUp(self):
        util._write_stream = io.StringIO()
        util._error_stream = io.StringIO()
        
    def tearDown(self):
        util._quiet = False
        util._write_stream = sys.stdout
        util._error_stream = sys.stderr

    def testWrite(self):
        s = 'test1'
        util.write(s)
        self.assertEqual(s, util._write_stream.getvalue())

    def testWriteQuiet(self):
        util.set_quiet(True)
        s = 'test2'
        util.write(s)
        self.assertEqual('', util._write_stream.getvalue())

    def testError(self):
        s = 'test3'
        util.error(s)
        self.assertEqual(s, util._error_stream.getvalue())

    def testErrorQuiet(self):
        s = 'test4'
        util.set_quiet(True)
        util.error(s)
        self.assertEqual(s, util._error_stream.getvalue())


class DummySection(util.BaseSection):
    HEX_LINE_LENGTH_BYTES = 3


class TestBaseSection(unittest.TestCase):
    def testInit(self):
        s = DummySection(b'abcdefgh', 4)
        self.assertEqual(b'abcdefgh', s._data)
        self.assertEqual(4, s._version)

    def testFromLines(self):
        lines = ['616263\n', '646566\n', '6768\n']
        s = DummySection.from_lines(lines, 4)
        self.assertEqual(b'abcdefgh', s._data)
        self.assertEqual(4, s._version)

    def testFromBytes(self):
        s = DummySection.from_bytes(b'abcdefgh', 4)
        self.assertEqual(b'abcdefgh', s._data)
        self.assertEqual(4, s._version)

    def testToLines(self):
        s = DummySection.from_bytes(b'abcdefgh', 4)
        lines = list(s.to_lines())
        self.assertEqual(['616263\n', '646566\n', '6768\n'], lines)

        
if __name__ == '__main__':
    unittest.main()
