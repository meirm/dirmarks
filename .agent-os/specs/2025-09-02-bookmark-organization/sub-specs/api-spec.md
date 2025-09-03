# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-09-02-bookmark-organization/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Endpoints

### Command-Line Interface Extensions

#### Add Bookmark with Category
```bash
dir --add <name> --category <category> --tags <tag1,tag2,tag3>
```

#### List Bookmarks with Filtering
```bash
dir -l --category <category>
dir -l --tag <tag>
dir -l --color
```

#### Update Bookmark Organization
```bash
dir --update <name> --category <new-category>
dir --update <name> --tags <new-tag1,new-tag2>
```

#### Category Management
```bash
dir --list-categories
dir --category-info <category>
```

## Controllers

### Marks Class Method Extensions

#### `add_mark(name, path, category=None, tags=None)`
- Enhanced to accept optional category and tags parameters
- Validates category name format (alphanumeric, hyphens, underscores, slashes)
- Stores tags as list of strings

#### `list_marks(category=None, tag=None, color=True)`
- Enhanced to filter by category or tag
- Returns formatted output with color coding when enabled
- Supports hierarchical category display with proper indentation

#### `update_mark(name, category=None, tags=None)`
- Updates organization metadata for existing bookmarks
- Preserves existing path and name information
- Validates new category and tag values

#### `get_categories()`
- Returns list of all categories currently in use
- Includes bookmark count per category
- Supports hierarchical category structure

#### `get_category_tree()`
- Returns hierarchical representation of categories
- Used for tree-like display formatting
- Calculates parent-child relationships from slash notation