#!/usr/bin/env python3
"""
Test suite for category and tag discovery commands.
Tests the new CLI commands for discovering available categories and tags.
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch

# Add the dirmarks module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirmarks.marks_enhanced import Marks
from dirmarks.main import main


class TestDiscoveryCommands(unittest.TestCase):
    """Test category and tag discovery functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
        self.marks = Marks()
        self.marks.rc = self.markrc_file
        # Clear any existing marks for isolated testing
        self.marks.marks = {}
        self.marks.marks_metadata = {}
        self.marks.list = []
        
        # Create test directories
        self.test_dirs = []
        for i in range(5):
            self.test_dirs.append(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        os.rmdir(self.temp_dir)
        
        for d in self.test_dirs:
            try:
                os.rmdir(d)
            except:
                pass
    
    def test_list_all_categories(self):
        """Test listing all unique categories."""
        # Add bookmarks with various categories
        self.marks.add_mark_with_category('proj1', self.test_dirs[0], 'work')
        self.marks.add_mark_with_category('proj2', self.test_dirs[1], 'work')
        self.marks.add_mark_with_category('photos', self.test_dirs[2], 'personal')
        self.marks.add_mark_with_category('config', self.test_dirs[3], 'work/devops')
        self.marks.add_mark('plain', self.test_dirs[4])  # No category
        
        categories = self.marks.list_all_categories()
        expected = ['personal', 'work', 'work/devops']
        self.assertEqual(categories, expected)
    
    def test_list_all_tags(self):
        """Test listing all unique tags."""
        # Add bookmarks with various tags
        self.marks.add_mark_with_tags('proj1', self.test_dirs[0], ['react', 'frontend'])
        self.marks.add_mark_with_tags('proj2', self.test_dirs[1], ['vue', 'frontend'])
        self.marks.add_mark_with_tags('proj3', self.test_dirs[2], ['python', 'backend', 'api'])
        self.marks.add_mark('plain', self.test_dirs[3])  # No tags
        
        tags = self.marks.list_all_tags()
        expected = ['api', 'backend', 'frontend', 'python', 'react', 'vue']
        self.assertEqual(tags, expected)
    
    def test_get_category_stats(self):
        """Test getting category usage statistics."""
        # Add bookmarks with categories
        self.marks.add_mark_with_category('proj1', self.test_dirs[0], 'work')
        self.marks.add_mark_with_category('proj2', self.test_dirs[1], 'work')
        self.marks.add_mark_with_category('proj3', self.test_dirs[2], 'work')
        self.marks.add_mark_with_category('photos', self.test_dirs[3], 'personal')
        
        stats = self.marks.get_category_stats()
        expected = {'personal': 1, 'work': 3}
        self.assertEqual(stats, expected)
    
    def test_get_tag_stats(self):
        """Test getting tag usage statistics."""
        # Add bookmarks with tags
        self.marks.add_mark_with_tags('proj1', self.test_dirs[0], ['frontend', 'react'])
        self.marks.add_mark_with_tags('proj2', self.test_dirs[1], ['frontend', 'vue'])
        self.marks.add_mark_with_tags('proj3', self.test_dirs[2], ['backend', 'python'])
        self.marks.add_mark_with_tags('proj4', self.test_dirs[3], ['frontend', 'mobile'])
        
        stats = self.marks.get_tag_stats()
        expected = {'backend': 1, 'frontend': 3, 'mobile': 1, 'python': 1, 'react': 1, 'vue': 1}
        self.assertEqual(stats, expected)
    
    def test_empty_categories_and_tags(self):
        """Test discovery with no categories or tags."""
        # Add plain bookmark without metadata
        self.marks.add_mark('plain', self.test_dirs[0])
        
        categories = self.marks.list_all_categories()
        tags = self.marks.list_all_tags()
        
        self.assertEqual(categories, [])
        self.assertEqual(tags, [])
        
        category_stats = self.marks.get_category_stats()
        tag_stats = self.marks.get_tag_stats()
        
        self.assertEqual(category_stats, {})
        self.assertEqual(tag_stats, {})


class TestDiscoveryCLI(unittest.TestCase):
    """Test CLI discovery commands."""
    
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
    
    def test_categories_command(self):
        """Test --categories CLI command."""
        # Add bookmarks with categories
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_category('proj1', self.test_dir, 'work')
        marks.add_mark_with_category('proj2', self.test_dir, 'personal')
        
        # Test --categories command
        with patch.object(sys, 'argv', ['dirmarks', '--categories']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass
        
        # Verify output
        printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
        output = ' '.join(printed_calls)
        self.assertIn('Available categories:', output)
        self.assertIn('personal', output)
        self.assertIn('work', output)
    
    def test_tags_command(self):
        """Test --tags CLI command."""
        # Add bookmarks with tags
        marks = Marks()
        marks.rc = self.markrc_file
        
        test_dir2 = tempfile.mkdtemp()
        try:
            marks.add_mark_with_tags('proj1', self.test_dir, ['react', 'frontend'])
            marks.add_mark_with_tags('proj2', test_dir2, ['python', 'backend'])
            
            # Test --tags command
            with patch.object(sys, 'argv', ['dirmarks', '--tags']):
                with patch('builtins.print') as mock_print:
                    try:
                        main()
                    except SystemExit:
                        pass
            
            # Verify output
            printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
            output = ' '.join(printed_calls)
            self.assertIn('Available tags:', output)
            self.assertIn('backend', output)
            self.assertIn('frontend', output)
            self.assertIn('python', output)
            self.assertIn('react', output)
        finally:
            os.rmdir(test_dir2)
    
    def test_stats_command(self):
        """Test --stats CLI command."""
        # Add bookmarks with categories and tags
        marks = Marks()
        marks.rc = self.markrc_file
        
        test_dir2 = tempfile.mkdtemp()
        try:
            marks.add_mark_with_category('proj1', self.test_dir, 'work')
            marks.add_mark_with_category('proj2', test_dir2, 'work')
            marks.add_mark_with_tags('proj3', self.test_dir, ['important'])
            marks.add_mark('plain', test_dir2)  # No metadata
            
            # Test --stats command
            with patch.object(sys, 'argv', ['dirmarks', '--stats']):
                with patch('builtins.print') as mock_print:
                    try:
                        main()
                    except SystemExit:
                        pass
            
            # Verify output
            printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
            output = ' '.join(printed_calls)
            
            self.assertIn('Bookmark Statistics:', output)
            self.assertIn('Categories', output)
            self.assertIn('work: 2', output)
            self.assertIn('Tags', output)
            self.assertIn('important: 1', output)
            self.assertIn('Total bookmarks:', output)
            self.assertIn('With categories:', output)
            self.assertIn('With tags:', output)
        finally:
            os.rmdir(test_dir2)
    
    def test_empty_discovery_commands(self):
        """Test discovery commands with no categories/tags."""
        # No bookmarks added, so should show empty results
        
        # Test --categories with no data
        with patch.object(sys, 'argv', ['dirmarks', '--categories']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass
        
        printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
        output = ' '.join(printed_calls)
        self.assertIn('No categories found.', output)
        
        # Test --tags with no data
        with patch.object(sys, 'argv', ['dirmarks', '--tags']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass
        
        printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
        output = ' '.join(printed_calls)
        self.assertIn('No tags found.', output)


if __name__ == '__main__':
    unittest.main()