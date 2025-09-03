# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-02-cross-platform-shell-support/spec.md

> Created: 2025-09-02
> Version: 1.0.0

## Technical Requirements

- Create PowerShell function module (.psm1) with Windows path handling
- Implement Fish shell function with Fish-specific syntax
- Add shell detection logic to identify current shell environment
- Implement bidirectional path translation (Unix <-> Windows)
- Handle WSL path mapping (/mnt/c/ <-> C:\)
- Create installation scripts for each shell type
- Support PowerShell Core (cross-platform) and Windows PowerShell
- Implement shell-specific completion/suggestion systems
- Handle special characters and spaces in paths for each shell
- Ensure Unicode support across all shells

## Approach

### PowerShell Implementation
- Create `Dirmarks.psm1` module with `Set-DirMark`, `Get-DirMark`, and `Remove-DirMark` cmdlets
- Implement tab completion using PowerShell's `Register-ArgumentCompleter`
- Handle both forward slashes and backslashes in path inputs
- Support PowerShell parameter binding and pipeline input

### Fish Shell Implementation
- Develop `dirmarks.fish` function file with Fish-native syntax
- Utilize Fish's completion system with `complete` command
- Implement Fish-specific error handling and output formatting
- Support Fish's command substitution and variable expansion

### Shell Detection Strategy
- Use `$SHELL` environment variable as primary detection method
- Fallback to process name inspection via `ps` or `Get-Process`
- Detect WSL environment through `/proc/version` or registry keys
- Implement platform-specific detection logic (Windows vs Unix)

### Path Translation Module
- Create bidirectional path converter supporting Unix/Windows formats
- Handle WSL mount points (`/mnt/c/` ↔ `C:\`)
- Preserve relative path semantics across platforms
- Support UNC paths and network drives on Windows

## External Dependencies

- **psutil** - Cross-platform process and system utilities
- **Justification:** Provides reliable shell detection and process information across different operating systems, essential for automatic shell identification