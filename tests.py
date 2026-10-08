import unittest
from unittest.mock import patch
import search
from pathlib import Path

class TestSearch(unittest.TestCase):
    # Greenpath Scenarios
    def test_parse_with_dir_no_mode_and_keywords(self):
        test_args = [
            'search.py',
            'doc',
            'once',
            'comment'
        ]

        with patch('sys.argv',test_args):
            path,keywords,mode = search.parse_args()

        self.assertEqual(path,Path('doc'))
        self.assertEqual(keywords,['once','comment'])
        self.assertEqual(mode,'or')

    def test_parse_with_mode_no_dir_and_keywords(self):
        test_args = [
            'search.py',
            '--and',
            'once'
        ]
        
        with patch('sys.argv',test_args):
            path,keywords,mode = search.parse_args()

        self.assertEqual(path,'./')
        self.assertEqual(keywords,['once'])
        self.assertEqual(mode,'and')

    def test_parse_with_mode_and_dir(self):
        test_args = [
            'search.py',
            '--and',
            'doc',
            'once'
        ]

        with patch('sys.argv',test_args):
            path,keywords,mode = search.parse_args()

        self.assertEqual(path,Path('doc'))
        self.assertEqual(keywords,['once'])
        self.assertEqual(mode,'and')

    def test_parse_wo_mode_or_dir(self):
        test_args = [
            'search.py',
            'once',
            'comment'
        ]

        with patch('sys.argv',test_args):
            path,keywords,mode = search.parse_args()

        self.assertEqual(path,'./')
        self.assertEqual(keywords,['once','comment'])
        self.assertEqual(mode,'or')

    # ----------------------------------------------------
    # Exception Scenarios
    def test_parse_with_invalid_mode(self):
        test_args = [
            'search.py',
            '--both'
        ]

        with patch('sys.argv',test_args):
            with self.assertRaises(SystemExit):
                path,keywords,mode = search.parse_args()

    def test_parse_with_no_args(self):
        test_args = [
            'search.py'
        ]

        with patch('sys.argv',test_args):
            with self.assertRaises(IndexError):
                path,keywords,mode = search.parse_args()
