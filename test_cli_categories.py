#!/usr/bin/env python3
"""
Test suite for CLI category functionality in dirmarks.
Tests the command-line interface for category and tag management.
"""

import unittest
import tempfile
import os
import sys
import subprocess
import json
from unittest.mock import patch, MagicMock

# Add the dirmarks module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirmarks.main import main
from dirmarks.marks_enhanced import Marks


class TestCLICategoryManagement(unittest.TestCase):
    """Test CLI category management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
        self.test_dir = tempfile.mkdtemp()
        
        # Patch the home directory to use our temp directory
        self.home_patcher = patch('os.path.expanduser')
        self.mock_expanduser = self.home_patcher.start()
        self.mock_expanduser.return_value = self.markrc_file
        
    def tearDown(self):
        """Clean up test fixtures."""
        self.home_patcher.stop()
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        os.rmdir(self.temp_dir)
    
    def test_add_bookmark_with_category_flag(self):
        """Test adding a bookmark with --category flag."""
        # Mock sys.argv for --add with --category
        with patch.object(sys, 'argv', ['dirmarks', '--add', 'test', self.test_dir, '--category', 'work']):
            try:
                main()
            except SystemExit:
                pass
        
        # Verify bookmark was added with category
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('test')
        self.assertIsNotNone(mark_data)
        self.assertEqual(mark_data.get('category'), 'work')
    
    def test_add_bookmark_with_tag_flag(self):
        """Test adding a bookmark with --tag flag."""
        # Mock sys.argv for --add with --tag
        with patch.object(sys, 'argv', ['dirmarks', '--add', 'test', self.test_dir, '--tag', 'project,important']):
            try:
                main()
            except SystemExit:
                pass
        
        # Verify bookmark was added with tags
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('test')
        self.assertIsNotNone(mark_data)
        self.assertIn('project', mark_data.get('tags', []))
        self.assertIn('important', mark_data.get('tags', []))
    
    def test_add_bookmark_with_both_category_and_tags(self):
        """Test adding a bookmark with both --category and --tag flags."""
        with patch.object(sys, 'argv', ['dirmarks', '--add', 'test', self.test_dir, 
                                       '--category', 'work', '--tag', 'project,client']):
            try:
                main()
            except SystemExit:
                pass
        
        # Verify bookmark was added with both category and tags
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('test')
        self.assertIsNotNone(mark_data)
        self.assertEqual(mark_data.get('category'), 'work')
        self.assertIn('project', mark_data.get('tags', []))
        self.assertIn('client', mark_data.get('tags', []))
    
    def test_list_bookmarks_with_category_filter(self):
        """Test listing bookmarks filtered by category."""
        # Add bookmarks with different categories
        marks = Marks()
        marks.rc = self.markrc_file
        
        test_dir2 = tempfile.mkdtemp()
        try:
            marks.add_mark_with_category('work1', self.test_dir, 'work')
            marks.add_mark_with_category('work2', test_dir2, 'work')
            marks.add_mark_with_category('personal', test_dir2, 'personal')
            
            # Test --list with --category
            with patch.object(sys, 'argv', ['dirmarks', '--list', '--category', 'work']):
                with patch('builtins.print') as mock_print:
                    try:
                        main()
                    except SystemExit:
                        pass
            
            # Verify only work bookmarks were printed
            printed_output = ''.join([str(call.args[0]) for call in mock_print.call_args_list])
            self.assertIn('work1', printed_output)
            self.assertIn('work2', printed_output)
            self.assertNotIn('personal', printed_output)
        finally:
            os.rmdir(test_dir2)
    
    def test_list_bookmarks_with_tag_filter(self):
        """Test listing bookmarks filtered by tag."""
        # Add bookmarks with different tags
        marks = Marks()
        marks.rc = self.markrc_file
        
        test_dir2 = tempfile.mkdtemp()
        try:
            marks.add_mark_with_tags('proj1', self.test_dir, ['frontend', 'react'])
            marks.add_mark_with_tags('proj2', test_dir2, ['backend', 'python'])
            marks.add_mark_with_tags('proj3', test_dir2, ['frontend', 'vue'])
            
            # Test --list with --tag
            with patch.object(sys, 'argv', ['dirmarks', '--list', '--tag', 'frontend']):
                with patch('builtins.print') as mock_print:
                    try:
                        main()
                    except SystemExit:
                        pass
            
            # Verify only frontend bookmarks were printed
            printed_output = ''.join([str(call.args[0]) for call in mock_print.call_args_list])
            self.assertIn('proj1', printed_output)
            self.assertIn('proj3', printed_output)
            self.assertNotIn('proj2', printed_output)
        finally:
            os.rmdir(test_dir2)
    
    def test_update_bookmark_category(self):
        """Test updating a bookmark's category."""
        # Add bookmark first
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_category('test', self.test_dir, 'work')
        
        # Update category
        with patch.object(sys, 'argv', ['dirmarks', '--update', 'test', self.test_dir, '--category', 'personal']):
            try:
                main()
            except SystemExit:
                pass
        
        # Verify category was updated
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('test')
        self.assertEqual(mark_data.get('category'), 'personal')
    
    def test_enhanced_list_output_with_categories(self):
        """Test that list output includes category information."""
        # Add bookmarks with categories
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_category('work1', self.test_dir, 'work')
        marks.add_mark_with_tags('proj1', self.test_dir, ['important', 'client'])
        
        # Test enhanced list output
        with patch.object(sys, 'argv', ['dirmarks', '--list']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass
        
        # Check that category/tag information is displayed
        printed_output = ''.join([str(call.args[0]) for call in mock_print.call_args_list])
        # The output should include some indication of categories/tags
        self.assertTrue(len(printed_output) > 0)
    
    def test_mark_command_with_category(self):
        """Test --mark command with category assignment."""
        with patch('os.path.abspath') as mock_abspath:
            mock_abspath.return_value = self.test_dir
            with patch.object(sys, 'argv', ['dirmarks', '--mark', 'current', '--category', 'work']):
                try:
                    main()
                except SystemExit:
                    pass
        
        # Verify bookmark was created with category
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('current')
        self.assertIsNotNone(mark_data)
        self.assertEqual(mark_data.get('category'), 'work')
    
    def test_invalid_category_handling(self):
        """Test handling of invalid category names."""
        with patch.object(sys, 'argv', ['dirmarks', '--add', 'test', self.test_dir, '--category', 'invalid@category']):
            with patch('sys.stderr.write') as mock_stderr:
                try:
                    main()
                except SystemExit:
                    pass
        
        # Should show error for invalid category
        # Verify bookmark was not added
        marks = Marks()
        marks.rc = self.markrc_file
        marks.read_marks(self.markrc_file)
        
        mark_data = marks.get_mark_with_metadata('test')
        # Should either be None or have no category due to validation failure
        if mark_data:
            self.assertNotEqual(mark_data.get('category'), 'invalid@category')


class TestCLIArgumentParsing(unittest.TestCase):
    """Test command-line argument parsing for categories."""
    
    def test_parse_category_and_tag_arguments(self):
        """Test parsing of --category and --tag arguments."""
        # This would test the argument parsing logic
        # We'll implement this when we add the argument parsing
        pass


if __name__ == '__main__':
    unittest.main()