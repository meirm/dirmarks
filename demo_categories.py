#!/usr/bin/env python3
"""
Demonstration of the new category and tag features in dirmarks.
"""

import tempfile
import os
from dirmarks.marks_enhanced import Marks


def demo():
    """Demonstrate the new category features."""
    print("=== Dirmarks Category Feature Demo ===\n")
    
    # Create a Marks instance
    marks = Marks()
    
    # Create some test directories
    test_dirs = []
    for i in range(5):
        test_dirs.append(tempfile.mkdtemp())
    
    print("1. Adding bookmarks with categories:")
    print("-" * 40)
    
    # Add bookmarks with categories
    marks.add_mark_with_category('project1', test_dirs[0], 'work')
    print(f"✓ Added 'project1' → {test_dirs[0]} [category: work]")
    
    marks.add_mark_with_category('project2', test_dirs[1], 'work')
    print(f"✓ Added 'project2' → {test_dirs[1]} [category: work]")
    
    marks.add_mark_with_category('photos', test_dirs[2], 'personal')
    print(f"✓ Added 'photos' → {test_dirs[2]} [category: personal]")
    
    marks.add_mark_with_tags('docs', test_dirs[3], ['important', 'reference'])
    print(f"✓ Added 'docs' → {test_dirs[3]} [tags: important, reference]")
    
    marks.add_mark_with_metadata('config', test_dirs[4], 
                                 category='work/devops', 
                                 tags=['server', 'production'])
    print(f"✓ Added 'config' → {test_dirs[4]} [category: work/devops, tags: server, production]")
    
    print("\n2. Listing bookmarks by category:")
    print("-" * 40)
    
    work_marks = marks.list_by_category('work')
    print(f"Work bookmarks ({len(work_marks)}):")
    for mark in work_marks:
        print(f"  - {mark['name']}: {mark['path']}")
    
    print("\n3. Listing bookmarks by tag:")
    print("-" * 40)
    
    important_marks = marks.list_by_tag('important')
    print(f"Bookmarks tagged 'important' ({len(important_marks)}):")
    for mark in important_marks:
        print(f"  - {mark['name']}: {mark['path']}")
    
    print("\n4. Category validation:")
    print("-" * 40)
    
    valid_categories = ['work', 'personal', 'project-1', 'client_abc']
    invalid_categories = ['work@home', 'project#1', 'my stuff']
    
    print("Valid categories:")
    for cat in valid_categories:
        result = marks.is_valid_category(cat)
        print(f"  '{cat}': {'✓' if result else '✗'}")
    
    print("\nInvalid categories:")
    for cat in invalid_categories:
        result = marks.is_valid_category(cat)
        print(f"  '{cat}': {'✓' if result else '✗'}")
    
    print("\n5. Setting category colors:")
    print("-" * 40)
    
    marks.set_category_color('work', 'blue')
    marks.set_category_color('personal', 'green')
    marks.set_category_color('important', 'red')
    
    print("Category colors configured:")
    print(f"  work → {marks.get_category_color('work')}")
    print(f"  personal → {marks.get_category_color('personal')}")
    print(f"  important → {marks.get_category_color('important')}")
    
    print("\n6. Backward compatibility:")
    print("-" * 40)
    
    # Old style bookmark (without category)
    marks.add_mark('oldstyle', test_dirs[0])
    old_data = marks.get_mark_with_metadata('oldstyle')
    print(f"Old-style bookmark 'oldstyle':")
    print(f"  Path: {old_data['path']}")
    print(f"  Category: {old_data.get('category', 'None')}")
    print(f"  Tags: {old_data.get('tags', [])}")
    
    # Clean up test directories
    for d in test_dirs:
        try:
            os.rmdir(d)
        except:
            pass
    
    print("\n=== Demo Complete ===")
    print("\nThe new category features are fully backward compatible.")
    print("Existing bookmarks continue to work without modification.")
    print("New bookmarks can include categories and tags for better organization.")


if __name__ == "__main__":
    demo()