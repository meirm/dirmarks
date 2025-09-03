#!/usr/bin/env python3
"""
Test suite for category and tag functionality in dirmarks.
Tests the new category-based bookmark organization features.
"""

import unittest
import tempfile
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Add the dirmarks module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirmarks.marks_enhanced import Marks


class TestCategoryStorage(unittest.TestCase):
    """Test category storage and retrieval functionality."""
    
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
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        os.rmdir(self.temp_dir)
    
    def test_add_mark_with_category(self):
        """Test adding a bookmark with a category."""
        # Create a real directory for testing
        test_dir = tempfile.mkdtemp()
        
        try:
            # Add bookmark with category
            result = self.marks.add_mark_with_category('test', test_dir, 'work')
            self.assertTrue(result)
            
            # Verify the bookmark was added with category
            mark_data = self.marks.get_mark_with_metadata('test')
            self.assertIsNotNone(mark_data)
            self.assertEqual(mark_data.get('path'), test_dir)
            self.assertEqual(mark_data.get('category'), 'work')
        finally:
            os.rmdir(test_dir)
    
    def test_add_mark_with_tags(self):
        """Test adding a bookmark with multiple tags."""
        test_dir = tempfile.mkdtemp()
        
        try:
            # Add bookmark with tags
            tags = ['project', 'client-a', 'frontend']
            result = self.marks.add_mark_with_tags('test', test_dir, tags)
            self.assertTrue(result)
            
            # Verify tags were added
            mark_data = self.marks.get_mark_with_metadata('test')
            self.assertIsNotNone(mark_data)
            self.assertEqual(set(mark_data.get('tags', [])), set(tags))
        finally:
            os.rmdir(test_dir)
    
    def test_category_validation(self):
        """Test category name validation."""
        test_dir = tempfile.mkdtemp()
        
        try:
            # Valid category names
            valid_names = ['work', 'project-1', 'client_abc', 'dev-env']
            for name in valid_names:
                self.assertTrue(self.marks.is_valid_category(name))
            
            # Invalid category names
            invalid_names = ['work@home', 'project#1', 'client abc', '']
            for name in invalid_names:
                self.assertFalse(self.marks.is_valid_category(name))
        finally:
            os.rmdir(test_dir)
    
    def test_hierarchical_categories(self):
        """Test hierarchical category support."""
        test_dir = tempfile.mkdtemp()
        
        try:
            # Add bookmark with hierarchical category
            result = self.marks.add_mark_with_category('test', test_dir, 'work/client-a/backend')
            self.assertTrue(result)
            
            # Verify hierarchical category structure
            mark_data = self.marks.get_mark_with_metadata('test')
            self.assertEqual(mark_data.get('category'), 'work/client-a/backend')
            
            # Test category path parsing
            category_parts = self.marks.parse_category_path('work/client-a/backend')
            self.assertEqual(category_parts, ['work', 'client-a', 'backend'])
        finally:
            os.rmdir(test_dir)
    
    def test_list_by_category(self):
        """Test filtering bookmarks by category."""
        # Create test directories
        dirs = []
        for i in range(3):
            dirs.append(tempfile.mkdtemp())
        
        try:
            # Add bookmarks with different categories
            self.marks.add_mark_with_category('work1', dirs[0], 'work')
            self.marks.add_mark_with_category('work2', dirs[1], 'work')
            self.marks.add_mark_with_category('personal', dirs[2], 'personal')
            
            # Filter by category
            work_marks = self.marks.list_by_category('work')
            self.assertEqual(len(work_marks), 2)
            self.assertIn('work1', [m['name'] for m in work_marks])
            self.assertIn('work2', [m['name'] for m in work_marks])
            
            personal_marks = self.marks.list_by_category('personal')
            self.assertEqual(len(personal_marks), 1)
            self.assertEqual(personal_marks[0]['name'], 'personal')
        finally:
            for d in dirs:
                os.rmdir(d)
    
    def test_list_by_tag(self):
        """Test filtering bookmarks by tag."""
        dirs = []
        for i in range(3):
            dirs.append(tempfile.mkdtemp())
        
        try:
            # Add bookmarks with different tags
            self.marks.add_mark_with_tags('proj1', dirs[0], ['frontend', 'react'])
            self.marks.add_mark_with_tags('proj2', dirs[1], ['backend', 'python'])
            self.marks.add_mark_with_tags('proj3', dirs[2], ['frontend', 'vue'])
            
            # Filter by tag
            frontend_marks = self.marks.list_by_tag('frontend')
            self.assertEqual(len(frontend_marks), 2)
            names = [m['name'] for m in frontend_marks]
            self.assertIn('proj1', names)
            self.assertIn('proj3', names)
        finally:
            for d in dirs:
                os.rmdir(d)
    
    def test_backward_compatibility(self):
        """Test backward compatibility with existing bookmark format."""
        test_dir = tempfile.mkdtemp()
        
        try:
            # Write old format bookmark
            with open(self.markrc_file, 'w') as f:
                f.write(f"oldmark:{test_dir}\n")
            
            # Read with new system
            marks = Marks()
            marks.rc = self.markrc_file
            marks.read_marks(self.markrc_file)
            
            # Should still work without category
            mark_data = marks.get_mark_with_metadata('oldmark')
            self.assertIsNotNone(mark_data)
            self.assertEqual(mark_data.get('path'), test_dir)
            self.assertIsNone(mark_data.get('category'))
            self.assertEqual(mark_data.get('tags', []), [])
        finally:
            os.rmdir(test_dir)
    
    def test_update_mark_category(self):
        """Test updating an existing bookmark's category."""
        test_dir = tempfile.mkdtemp()
        
        try:
            # Add initial bookmark
            self.marks.add_mark_with_category('test', test_dir, 'work')
            
            # Update category
            result = self.marks.update_mark_category('test', 'personal')
            self.assertTrue(result)
            
            # Verify update
            mark_data = self.marks.get_mark_with_metadata('test')
            self.assertEqual(mark_data.get('category'), 'personal')
        finally:
            os.rmdir(test_dir)
    
    def test_category_color_configuration(self):
        """Test category color configuration storage."""
        # Set color for category
        self.marks.set_category_color('work', 'blue')
        self.marks.set_category_color('personal', 'green')
        
        # Retrieve colors
        self.assertEqual(self.marks.get_category_color('work'), 'blue')
        self.assertEqual(self.marks.get_category_color('personal'), 'green')
        self.assertEqual(self.marks.get_category_color('unknown'), 'default')


class TestCategoryFileFormat(unittest.TestCase):
    """Test the new file format with category support."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        os.rmdir(self.temp_dir)
    
    def test_new_file_format_write(self):
        """Test writing bookmarks in new format with metadata."""
        test_dir = tempfile.mkdtemp()
        
        try:
            marks = Marks()
            marks.rc = self.markrc_file
            
            # Add bookmark with metadata
            marks.add_mark_with_metadata('test', test_dir, 
                                        category='work',
                                        tags=['project', 'important'])
            
            # Read file and verify format
            with open(self.markrc_file, 'r') as f:
                content = f.read()
                # Should contain JSON metadata
                self.assertIn('test:', content)
                self.assertIn(test_dir, content)
                # The new format should include metadata
                lines = content.strip().split('\n')
                self.assertTrue(any('category' in line or 'work' in line for line in lines))
        finally:
            os.rmdir(test_dir)
    
    def test_mixed_format_compatibility(self):
        """Test reading files with both old and new format entries."""
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()
        
        try:
            # Write mixed format file
            with open(self.markrc_file, 'w') as f:
                # Old format
                f.write(f"old:{dir1}\n")
                # New format with metadata (JSON on second line)
                f.write(f"new:{dir2}|category:work|tags:project,client\n")
            
            # Read with new system
            marks = Marks()
            marks.rc = self.markrc_file
            marks.read_marks_with_metadata(self.markrc_file)
            
            # Both should work
            old_data = marks.get_mark_with_metadata('old')
            self.assertEqual(old_data.get('path'), dir1)
            self.assertIsNone(old_data.get('category'))
            
            new_data = marks.get_mark_with_metadata('new')
            self.assertEqual(new_data.get('path'), dir2)
            self.assertEqual(new_data.get('category'), 'work')
            self.assertIn('project', new_data.get('tags', []))
        finally:
            os.rmdir(dir1)
            os.rmdir(dir2)


if __name__ == '__main__':
    unittest.main()