# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-09-02-import-export-functionality/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Command Line Interface

### Export Commands

```bash
# Export all bookmarks to JSON
dirmarks --export bookmarks.json

# Export all bookmarks to YAML
dirmarks --export bookmarks.yaml

# Export all bookmarks to CSV
dirmarks --export bookmarks.csv

# Export specific category
dirmarks --export project-bookmarks.json --category work

# Export multiple categories
dirmarks --export filtered-bookmarks.yaml --category "work,personal"

# Export with tags filter
dirmarks --export tagged-bookmarks.json --tags "important,frequent"
```

### Import Commands

```bash
# Import bookmarks (replace existing)
dirmarks --import bookmarks.json

# Import bookmarks (merge with existing)
dirmarks --import bookmarks.yaml --merge

# Import bookmarks (selective mode - prompt for conflicts)
dirmarks --import bookmarks.csv --selective

# Import with dry-run (show what would be imported)
dirmarks --import bookmarks.json --dry-run

# Import with backup of existing bookmarks
dirmarks --import bookmarks.yaml --backup
```

## Internal API Methods

### Export Module

```python
class BookmarkExporter:
    def export_bookmarks(self, 
                        filename: str, 
                        format: str = None,
                        category: str = None,
                        tags: List[str] = None) -> bool
    
    def _serialize_json(self, bookmarks: List[Bookmark]) -> str
    def _serialize_yaml(self, bookmarks: List[Bookmark]) -> str  
    def _serialize_csv(self, bookmarks: List[Bookmark]) -> str
    
    def _filter_by_category(self, bookmarks: List[Bookmark], category: str) -> List[Bookmark]
    def _filter_by_tags(self, bookmarks: List[Bookmark], tags: List[str]) -> List[Bookmark]
```

### Import Module

```python
class BookmarkImporter:
    def import_bookmarks(self,
                        filename: str,
                        strategy: str = "replace",  # replace, merge, selective
                        dry_run: bool = False,
                        backup: bool = True) -> ImportResult
    
    def _deserialize_json(self, content: str) -> List[Bookmark]
    def _deserialize_yaml(self, content: str) -> List[Bookmark]
    def _deserialize_csv(self, content: str) -> List[Bookmark]
    
    def _translate_paths(self, bookmarks: List[Bookmark]) -> List[Bookmark]
    def _detect_conflicts(self, new_bookmarks: List[Bookmark], existing: List[Bookmark]) -> List[Conflict]
    def _resolve_conflicts(self, conflicts: List[Conflict], strategy: str) -> List[Bookmark]
```

## Data Formats

### JSON Format
```json
{
  "version": "1.0.0",
  "export_date": "2025-09-02T10:30:00Z",
  "total_bookmarks": 42,
  "bookmarks": [
    {
      "name": "project",
      "path": "/home/user/projects/myapp",
      "category": "work",
      "tags": ["important", "daily"],
      "created_date": "2025-01-15T09:00:00Z",
      "usage_count": 156
    }
  ]
}
```

### YAML Format
```yaml
version: "1.0.0"
export_date: "2025-09-02T10:30:00Z"
total_bookmarks: 42
bookmarks:
  - name: "project"
    path: "/home/user/projects/myapp"
    category: "work"
    tags: ["important", "daily"]
    created_date: "2025-01-15T09:00:00Z"
    usage_count: 156
```

### CSV Format
```csv
name,path,category,tags,created_date,usage_count
project,/home/user/projects/myapp,work,"important,daily",2025-01-15T09:00:00Z,156
```