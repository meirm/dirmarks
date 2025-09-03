# Database Schema

This is the database schema implementation for the spec detailed in @.agent-os/specs/2025-09-02-bookmark-organization/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Schema Changes

### Bookmark Entry Format

```json
{
  "name": "bookmark-name",
  "path": "/absolute/path/to/directory",
  "category": "work/projects",
  "tags": ["python", "web", "backend"],
  "created_at": "2025-09-02T10:30:00Z",
  "updated_at": "2025-09-02T10:30:00Z"
}
```

### Legacy Compatibility

Existing bookmarks without category/tags fields will be handled gracefully:

```json
{
  "name": "old-bookmark",
  "path": "/path/to/dir"
}
```

Default behavior:
- `category`: null or "uncategorized"
- `tags`: empty array []

### Configuration Schema

```json
{
  "categories": {
    "work": {
      "color": "blue",
      "description": "Work-related projects"
    },
    "personal": {
      "color": "green", 
      "description": "Personal projects"
    }
  },
  "default_category": "uncategorized",
  "color_enabled": true
}
```

## Migrations

1. **Migration v1.0 → v1.1**: Add optional category and tags fields to existing bookmark entries
2. **Backward Compatibility**: Maintain support for reading bookmarks without organization metadata
3. **Configuration Setup**: Initialize default category color configuration on first run