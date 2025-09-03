#!/usr/bin/env python3
"""
Test suite for advanced category filtering and listing functionality.
Tests hierarchical categories, complex filtering, and edge cases.
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch

# Add the dirmarks module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirmarks.marks_enhanced import Marks
from dirmarks.main import enhanced_list_marks, main


class TestAdvancedCategoryFiltering(unittest.TestCase):
    """Test advanced category filtering functionality."""
    
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
        for i in range(10):
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
    
    def test_hierarchical_category_filtering(self):
        """Test filtering with hierarchical categories."""
        # Add bookmarks with hierarchical categories
        self.marks.add_mark_with_category('web1', self.test_dirs[0], 'work/web/frontend')
        self.marks.add_mark_with_category('web2', self.test_dirs[1], 'work/web/backend')
        self.marks.add_mark_with_category('mobile1', self.test_dirs[2], 'work/mobile/ios')
        self.marks.add_mark_with_category('mobile2', self.test_dirs[3], 'work/mobile/android')
        self.marks.add_mark_with_category('personal1', self.test_dirs[4], 'personal/photos')
        
        # Test exact category match
        web_frontend = self.marks.list_by_category('work/web/frontend')
        self.assertEqual(len(web_frontend), 1)
        self.assertEqual(web_frontend[0]['name'], 'web1')
        
        # Test different hierarchical levels
        mobile_ios = self.marks.list_by_category('work/mobile/ios')
        self.assertEqual(len(mobile_ios), 1)
        self.assertEqual(mobile_ios[0]['name'], 'mobile1')
        
        personal_photos = self.marks.list_by_category('personal/photos')
        self.assertEqual(len(personal_photos), 1)
        self.assertEqual(personal_photos[0]['name'], 'personal1')
    
    def test_category_hierarchy_parsing(self):
        """Test category path parsing for hierarchical categories."""
        # Test parsing different hierarchy levels
        test_cases = [
            ('work', ['work']),
            ('work/client-a', ['work', 'client-a']),
            ('work/client-a/backend', ['work', 'client-a', 'backend']),
            ('personal/projects/side-hustle', ['personal', 'projects', 'side-hustle'])
        ]
        
        for category_path, expected_parts in test_cases:
            parts = self.marks.parse_category_path(category_path)
            self.assertEqual(parts, expected_parts, 
                           f"Failed to parse {category_path} correctly")
    
    def test_multiple_tag_filtering(self):
        """Test filtering bookmarks with multiple tag combinations."""
        # Add bookmarks with various tag combinations
        self.marks.add_mark_with_tags('proj1', self.test_dirs[0], ['react', 'frontend', 'client-a'])
        self.marks.add_mark_with_tags('proj2', self.test_dirs[1], ['vue', 'frontend', 'client-b'])
        self.marks.add_mark_with_tags('proj3', self.test_dirs[2], ['node', 'backend', 'client-a'])
        self.marks.add_mark_with_tags('proj4', self.test_dirs[3], ['python', 'backend', 'client-b'])
        self.marks.add_mark_with_tags('proj5', self.test_dirs[4], ['react', 'backend', 'fullstack'])
        
        # Test filtering by different tags
        frontend_projects = self.marks.list_by_tag('frontend')
        self.assertEqual(len(frontend_projects), 2)
        frontend_names = [p['name'] for p in frontend_projects]
        self.assertIn('proj1', frontend_names)
        self.assertIn('proj2', frontend_names)
        
        client_a_projects = self.marks.list_by_tag('client-a')
        self.assertEqual(len(client_a_projects), 2)
        client_a_names = [p['name'] for p in client_a_projects]
        self.assertIn('proj1', client_a_names)
        self.assertIn('proj3', client_a_names)
        
        react_projects = self.marks.list_by_tag('react')
        self.assertEqual(len(react_projects), 2)
        react_names = [p['name'] for p in react_projects]
        self.assertIn('proj1', react_names)
        self.assertIn('proj5', react_names)
    
    def test_combined_category_and_tag_bookmarks(self):
        """Test bookmarks with both categories and tags."""
        # Add bookmarks with both categories and tags
        self.marks.add_mark_with_metadata('webapp', self.test_dirs[0], 
                                         category='work/web', 
                                         tags=['react', 'client-a', 'production'])
        self.marks.add_mark_with_metadata('api', self.test_dirs[1], 
                                         category='work/backend', 
                                         tags=['node', 'client-a', 'production'])
        self.marks.add_mark_with_metadata('mobile', self.test_dirs[2], 
                                         category='work/mobile', 
                                         tags=['flutter', 'client-b', 'development'])
        
        # Test category filtering
        web_projects = self.marks.list_by_category('work/web')
        self.assertEqual(len(web_projects), 1)
        self.assertEqual(web_projects[0]['name'], 'webapp')
        self.assertIn('react', web_projects[0]['tags'])
        
        # Test tag filtering
        client_a_projects = self.marks.list_by_tag('client-a')
        self.assertEqual(len(client_a_projects), 2)
        names = [p['name'] for p in client_a_projects]
        self.assertIn('webapp', names)
        self.assertIn('api', names)
        
        production_projects = self.marks.list_by_tag('production')
        self.assertEqual(len(production_projects), 2)
    
    def test_case_sensitive_filtering(self):
        """Test that category and tag filtering is case-sensitive."""
        self.marks.add_mark_with_category('test1', self.test_dirs[0], 'Work')
        self.marks.add_mark_with_category('test2', self.test_dirs[1], 'work')
        self.marks.add_mark_with_tags('test3', self.test_dirs[2], ['Important', 'urgent'])
        self.marks.add_mark_with_tags('test4', self.test_dirs[3], ['important', 'urgent'])
        
        # Case-sensitive category filtering
        work_upper = self.marks.list_by_category('Work')
        work_lower = self.marks.list_by_category('work')
        self.assertEqual(len(work_upper), 1)
        self.assertEqual(len(work_lower), 1)
        self.assertNotEqual(work_upper[0]['name'], work_lower[0]['name'])
        
        # Case-sensitive tag filtering
        important_upper = self.marks.list_by_tag('Important')
        important_lower = self.marks.list_by_tag('important')
        self.assertEqual(len(important_upper), 1)
        self.assertEqual(len(important_lower), 1)
        self.assertNotEqual(important_upper[0]['name'], important_lower[0]['name'])
    
    def test_empty_filtering_results(self):
        """Test filtering with non-existent categories and tags."""
        # Add some bookmarks
        self.marks.add_mark_with_category('test1', self.test_dirs[0], 'work')
        self.marks.add_mark_with_tags('test2', self.test_dirs[1], ['important'])
        
        # Test non-existent category
        nonexistent = self.marks.list_by_category('nonexistent')
        self.assertEqual(len(nonexistent), 0)
        
        # Test non-existent tag
        nonexistent = self.marks.list_by_tag('nonexistent')
        self.assertEqual(len(nonexistent), 0)
    
    def test_enhanced_list_output_formatting(self):
        """Test the enhanced list output formatting."""
        # Add bookmarks with various combinations
        self.marks.add_mark_with_metadata('complex', self.test_dirs[0], 
                                         category='work/client-a/backend', 
                                         tags=['python', 'api', 'production', 'critical'])
        self.marks.add_mark_with_category('simple', self.test_dirs[1], 'personal')
        self.marks.add_mark_with_tags('tagged', self.test_dirs[2], ['temp', 'testing'])
        self.marks.add_mark('plain', self.test_dirs[3])  # No category or tags
        
        # Test category filtering with enhanced output
        with patch('builtins.print') as mock_print:
            enhanced_list_marks(self.marks, category_filter='work/client-a/backend')
            
            # Verify output was printed
            self.assertTrue(mock_print.called)
            calls = [str(call.args[0]) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('complex', output)
            self.assertIn('python', output)
            self.assertIn('api', output)
        
        # Test tag filtering with enhanced output
        with patch('builtins.print') as mock_print:
            enhanced_list_marks(self.marks, tag_filter='temp')
            
            self.assertTrue(mock_print.called)
            calls = [str(call.args[0]) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('tagged', output)
            self.assertIn('testing', output)


class TestCLIAdvancedFiltering(unittest.TestCase):
    """Test CLI advanced filtering functionality."""
    
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
    
    def test_hierarchical_category_cli_filtering(self):
        """Test CLI filtering with hierarchical categories."""
        # Create bookmarks with hierarchical categories
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_category('webapp', self.test_dir, 'work/web/frontend')
        marks.add_mark_with_category('api', self.test_dir, 'work/api/backend')
        
        # Test CLI filtering for hierarchical category
        with patch.object(sys, 'argv', ['dirmarks', '--list', '--category', 'work/web/frontend']):
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except SystemExit:
                    pass
        
        # Verify the correct bookmark was shown
        printed_output = ''.join([str(call.args[0]) for call in mock_print.call_args_list])
        self.assertIn('webapp', printed_output)
        self.assertNotIn('api', printed_output)
    
    def test_complex_tag_combinations_cli(self):
        """Test CLI filtering with complex tag combinations."""
        marks = Marks()
        marks.rc = self.markrc_file
        
        test_dir2 = tempfile.mkdtemp()
        try:
            marks.add_mark_with_tags('frontend', self.test_dir, ['react', 'client-a', 'production'])
            marks.add_mark_with_tags('backend', test_dir2, ['node', 'client-a', 'production'])
            marks.add_mark_with_tags('mobile', test_dir2, ['flutter', 'client-b', 'development'])
            
            # Test filtering by production tag
            with patch.object(sys, 'argv', ['dirmarks', '--list', '--tag', 'production']):
                with patch('builtins.print') as mock_print:
                    try:
                        main()
                    except SystemExit:
                        pass
            
            printed_output = ''.join([str(call.args[0]) for call in mock_print.call_args_list])
            self.assertIn('frontend', printed_output)
            self.assertIn('backend', printed_output)
            self.assertNotIn('mobile', printed_output)
        finally:
            os.rmdir(test_dir2)


if __name__ == '__main__':
    unittest.main()