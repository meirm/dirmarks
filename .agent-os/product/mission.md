# Product Mission

> Last Updated: 2025-09-02
> Version: 1.0.0

## Pitch

Dirmarks is a filesystem bookmarking tool that eliminates the pain of repetitive typing and remembering complex directory paths in the CLI. Instead of typing `cd /very/long/path/to/project/subdirectory` repeatedly, users can bookmark it as `proj` and simply type `dm proj` to instantly navigate there. It's like browser bookmarks, but for your filesystem.

## Users

**Primary Users:**
- Command-line power users who spend significant time navigating directories
- System administrators managing multiple server environments and configuration paths
- Software developers working across multiple projects with deep directory structures
- DevOps engineers switching between different deployment environments

**Secondary Users:**
- Data scientists working with complex dataset hierarchies
- Students learning command-line tools and file system navigation
- Technical writers organizing documentation across multiple project folders

## The Problem

CLI users waste significant time and mental energy on repetitive directory navigation:

1. **Repetitive Typing**: Constantly typing long, complex paths like `/usr/local/share/applications/custom/configs/environment-specific/`
2. **Memory Burden**: Trying to remember dozens of frequently-used paths across projects
3. **Context Switching**: Losing productivity when jumping between different project directories
4. **Error-Prone Navigation**: Typos in long paths leading to "directory not found" errors
5. **Inefficient Workflow**: Breaking concentration to recall or reconstruct directory paths
6. **Poor Organization**: No semantic structure for managing filesystem locations

Traditional solutions like shell aliases are limited, hard to manage, and don't scale well across multiple environments.

## Differentiators

**vs Shell Aliases:**
- Persistent storage with organized management (add, list, delete, update)
- Index-based navigation for quick access
- Cross-shell compatibility (bash/zsh)
- Semantic bookmark names vs cryptic alias names

**vs cd with Tab Completion:**
- Instant navigation without path reconstruction
- Works regardless of current directory location  
- Semantic naming independent of filesystem structure
- No need to remember partial paths for tab completion

**vs Built-in Shell History:**
- Persistent across sessions and shell restarts
- Organized by purpose rather than chronological order
- Direct bookmark management commands
- Cross-system portability through export/import

## Key Features

**Core Navigation:**
- One-command directory bookmarking: `dm add project-name`
- Instant navigation by name: `dm project-name` 
- Index-based quick access: `dm 1`, `dm 2`
- Current directory marking: `dm mark current-task`

**Management & Organization:**
- List all bookmarks with clear indices: `dm list`
- Update existing bookmarks: `dm update project-name /new/path`
- Remove obsolete bookmarks: `dm delete project-name`
- Path display without navigation: `dm path project-name`

**Cross-Environment Support:**
- Bash and Zsh shell compatibility
- System-wide and user-specific bookmark storage
- Easy installation via pip
- Portable bookmark collections