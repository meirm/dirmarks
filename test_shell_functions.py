#!/usr/bin/env python3
"""
Test suite for shell function compatibility and integration.
Tests the shell function integration with category and tag features.
"""

import unittest
import tempfile
import os
import sys
import subprocess
from unittest.mock import patch

# Add the dirmarks module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dirmarks.marks_enhanced import Marks


class TestShellFunctionCompatibility(unittest.TestCase):
    """Test shell function compatibility with enhanced features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
        self.test_dirs = [tempfile.mkdtemp() for _ in range(5)]
        
        # Create marks instance for setup
        self.marks = Marks()
        self.marks.rc = self.markrc_file
        
        # Set up test bookmarks with categories and tags
        self.marks.add_mark_with_metadata('project1', self.test_dirs[0], 
                                         category='work', tags=['urgent', 'frontend'])
        self.marks.add_mark_with_metadata('project2', self.test_dirs[1], 
                                         category='work', tags=['backend'])
        self.marks.add_mark_with_metadata('docs', self.test_dirs[2], 
                                         category='personal', tags=['important'])
        self.marks.add_mark('plain', self.test_dirs[3])  # No metadata
    
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
    
    def test_basic_shell_function_commands(self):
        """Test basic shell function commands still work with enhanced backend."""
        # Test that existing shell function commands work with enhanced marks
        
        # Patch expanduser to use our test markrc
        with patch('os.path.expanduser', return_value=self.markrc_file):
            # Test -l (list) command
            result = subprocess.run([sys.executable, '-m', 'dirmarks.main', '--list'], 
                                  capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn('project1', result.stdout)
            self.assertIn('work', result.stdout)  # Should show category
            
            # Test -p (print path) command
            result = subprocess.run([sys.executable, '-m', 'dirmarks.main', '--get', 'project1'], 
                                  capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), self.test_dirs[0])
            
            # Test -d (delete) command - create a temp bookmark to delete
            temp_dir = tempfile.mkdtemp()
            try:
                self.marks.add_mark('temp_delete', temp_dir)
                result = subprocess.run([sys.executable, '-m', 'dirmarks.main', '--delete', 'temp_delete'], 
                                      capture_output=True, text=True)
                self.assertEqual(result.returncode, 0)
                
                # Verify it's deleted
                self.assertIsNone(self.marks.get_mark('temp_delete'))
            finally:
                os.rmdir(temp_dir)
    
    def test_enhanced_add_commands_compatibility(self):
        """Test that enhanced add commands work through shell interface."""
        temp_dir = tempfile.mkdtemp()
        try:
            # Test adding with category via --add command
            result = subprocess.run([
                sys.executable, '-m', 'dirmarks.main', 
                '--add', 'test_cat', temp_dir, '--category', 'testing'
            ], capture_output=True, text=True,
            env={**os.environ, 'HOME': self.temp_dir})
            self.assertEqual(result.returncode, 0)
            
            # Verify it was added with category
            marks = Marks()
            marks.rc = self.markrc_file
            mark_data = marks.get_mark_with_metadata('test_cat')
            self.assertIsNotNone(mark_data)
            self.assertEqual(mark_data['category'], 'testing')
            
            # Test adding with tags via --add command
            result = subprocess.run([
                sys.executable, '-m', 'dirmarks.main', 
                '--add', 'test_tag', temp_dir, '--tag', 'urgent,testing'
            ], capture_output=True, text=True,
            env={**os.environ, 'HOME': self.temp_dir})
            self.assertEqual(result.returncode, 0)
            
            # Verify it was added with tags
            marks = Marks()
            marks.rc = self.markrc_file
            mark_data = marks.get_mark_with_metadata('test_tag')
            self.assertIsNotNone(mark_data)
            self.assertEqual(set(mark_data['tags']), {'urgent', 'testing'})
            
        finally:
            os.rmdir(temp_dir)
    
    def test_update_commands_compatibility(self):
        """Test that update commands work with category/tag features."""
        temp_dir = tempfile.mkdtemp()
        try:
            # First add a simple bookmark
            self.marks.add_mark('test_update', temp_dir)
            
            # Test updating with category
            result = subprocess.run([
                sys.executable, '-m', 'dirmarks.main', 
                '--update', 'test_update', temp_dir, '--category', 'updated'
            ], capture_output=True, text=True,
            env={**os.environ, 'HOME': self.temp_dir})
            self.assertEqual(result.returncode, 0)
            
            # Verify category was added
            marks = Marks()
            marks.rc = self.markrc_file
            mark_data = marks.get_mark_with_metadata('test_update')
            self.assertIsNotNone(mark_data)
            self.assertEqual(mark_data['category'], 'updated')
            
            # Test updating with tags
            result = subprocess.run([
                sys.executable, '-m', 'dirmarks.main', 
                '--update', 'test_update', temp_dir, '--tag', 'updated,test'
            ], capture_output=True, text=True,
            env={**os.environ, 'HOME': self.temp_dir})
            self.assertEqual(result.returncode, 0)
            
            # Verify tags were added
            marks = Marks()
            marks.rc = self.markrc_file
            mark_data = marks.get_mark_with_metadata('test_update')
            self.assertIsNotNone(mark_data)
            self.assertEqual(set(mark_data['tags']), {'updated', 'test'})
            
        finally:
            os.rmdir(temp_dir)
    
    def test_backward_compatibility(self):
        """Test that old shell function usage still works."""
        # Test that bookmarks without categories/tags still work
        result = subprocess.run([sys.executable, '-m', 'dirmarks.main', '--get', 'plain'], 
                              capture_output=True, text=True,
                              env={**os.environ, 'HOME': self.temp_dir})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), self.test_dirs[3])
        
        # Test that listing still works and shows both old and new format
        result = subprocess.run([sys.executable, '-m', 'dirmarks.main', '--list'], 
                              capture_output=True, text=True,
                              env={**os.environ, 'HOME': self.temp_dir})
        self.assertEqual(result.returncode, 0)
        self.assertIn('plain', result.stdout)  # Old format bookmark
        self.assertIn('project1', result.stdout)  # New format bookmark
        self.assertIn('work', result.stdout)  # Should show categories


class TestShellFunctionEnhancements(unittest.TestCase):
    """Test new shell function enhancements for categories and tags."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        os.rmdir(self.temp_dir)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_category_filtering_through_shell(self):
        """Test category filtering works through shell interface."""
        # Set up bookmarks with categories
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_metadata('work1', self.test_dir, category='work')
        marks.add_mark_with_metadata('work2', self.test_dir, category='work')
        marks.add_mark_with_metadata('personal1', self.test_dir, category='personal')
        
        # Test category filtering
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', 
            '--list', '--category', 'work'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('work1', result.stdout)
        self.assertIn('work2', result.stdout)
        self.assertNotIn('personal1', result.stdout)
    
    def test_tag_filtering_through_shell(self):
        """Test tag filtering works through shell interface."""
        # Set up bookmarks with tags
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_metadata('urgent1', self.test_dir, tags=['urgent', 'work'])
        marks.add_mark_with_metadata('urgent2', self.test_dir, tags=['urgent', 'personal'])
        marks.add_mark_with_metadata('normal', self.test_dir, tags=['work'])
        
        # Test tag filtering
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', 
            '--list', '--tag', 'urgent'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('urgent1', result.stdout)
        self.assertIn('urgent2', result.stdout)
        self.assertNotIn('normal', result.stdout)
    
    def test_discovery_commands_through_shell(self):
        """Test discovery commands work through shell interface."""
        # Set up diverse bookmarks
        marks = Marks()
        marks.rc = self.markrc_file
        marks.add_mark_with_metadata('test1', self.test_dir, category='work', tags=['urgent'])
        marks.add_mark_with_metadata('test2', self.test_dir, category='personal', tags=['important'])
        
        # Test --categories command
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', '--categories'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('work', result.stdout)
        self.assertIn('personal', result.stdout)
        
        # Test --tags command
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', '--tags'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('urgent', result.stdout)
        self.assertIn('important', result.stdout)
        
        # Test --stats command
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', '--stats'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Statistics', result.stdout)
        self.assertIn('work', result.stdout)
        self.assertIn('urgent', result.stdout)


class TestShellFunctionErrorHandling(unittest.TestCase):
    """Test error handling in shell function integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.markrc_file = os.path.join(self.temp_dir, '.markrc')
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.markrc_file):
            os.remove(self.markrc_file)
        os.rmdir(self.temp_dir)
    
    def test_invalid_category_handling(self):
        """Test handling of invalid categories through shell."""
        temp_dir = tempfile.mkdtemp()
        try:
            # Test adding bookmark with invalid category
            result = subprocess.run([
                sys.executable, '-m', 'dirmarks.main', 
                '--add', 'test', temp_dir, '--category', 'invalid@category'
            ], capture_output=True, text=True,
            env={**os.environ, 'HOME': self.temp_dir})
            
            # Should fail with invalid category
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Invalid category', result.stderr)
            
        finally:
            os.rmdir(temp_dir)
    
    def test_nonexistent_bookmark_handling(self):
        """Test handling of operations on non-existent bookmarks."""
        # Test getting non-existent bookmark
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', '--get', 'nonexistent'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not found', result.stderr)
        
        # Test deleting non-existent bookmark
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', '--delete', 'nonexistent'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        # Delete operations typically succeed even for non-existent items
        # but we should handle it gracefully
        self.assertTrue(result.returncode in [0, 1])  # Either succeeds or fails gracefully
    
    def test_empty_filtering_results(self):
        """Test handling of empty filtering results."""
        # Test filtering with no matches
        result = subprocess.run([
            sys.executable, '-m', 'dirmarks.main', 
            '--list', '--category', 'nonexistent'
        ], capture_output=True, text=True,
        env={**os.environ, 'HOME': self.temp_dir})
        
        self.assertEqual(result.returncode, 0)
        # Should handle empty results gracefully
        self.assertIn('category', result.stdout.lower())


if __name__ == '__main__':
    unittest.main()