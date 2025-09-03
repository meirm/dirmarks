# Spec Requirements Document

> Spec: Cross-Platform Shell Support
> Created: 2025-09-02
> Status: Planning

## Overview

Implement comprehensive shell compatibility across PowerShell (Windows), Fish shell, and other popular shells to make Dirmarks truly cross-platform. This feature will ensure consistent bookmark functionality regardless of the user's shell preference or operating system, expanding the tool's reach to Windows users and alternative shell enthusiasts.

## User Stories

### Windows PowerShell Integration

As a Windows developer, I want to use Dirmarks in PowerShell, so that I can have the same bookmark functionality I use on Linux systems.

When I install Dirmarks on Windows, I can add a PowerShell function to my profile that provides the same `dir` command interface. The function handles Windows path formats (C:\Users\...) and PowerShell-specific syntax while maintaining compatibility with the core Python backend.

### Fish Shell Compatibility

As a Fish shell user, I want native Dirmarks integration, so that I can use bookmarks with Fish's modern syntax and features.

After installing Dirmarks, I can source a Fish-specific function file that provides bookmark commands using Fish's function syntax. The integration takes advantage of Fish features like autosuggestions and completions for bookmark names.

### Universal Shell Framework

As a user who switches between different shells, I want consistent bookmark behavior across all shells, so that my muscle memory works everywhere.

Whether I'm using Bash, Zsh, PowerShell, or Fish, the core commands remain the same: `dir bookmark-name` to navigate, `dir -l` to list, `dir -a name path` to add. The implementation handles shell-specific differences transparently.

## Spec Scope

1. **PowerShell Function** - Native PowerShell function with Windows path support
2. **Fish Shell Function** - Fish-compatible function with completions
3. **Shell Detection** - Automatic shell detection and appropriate function installation
4. **Path Translation** - Seamless conversion between Unix and Windows path formats
5. **WSL Integration** - Special handling for Windows Subsystem for Linux environments

## Out of Scope

- Exotic or rarely-used shells (tcsh, ksh, etc.)
- Shell-specific advanced features beyond core functionality
- GUI shell integration (Windows Terminal settings, etc.)
- Shell plugin managers integration
- Command abbreviation or shell-specific aliases

## Expected Deliverable

1. PowerShell users can use Dirmarks with native Windows path support
2. Fish shell users have full bookmark functionality with completions
3. Installation script detects shell and installs appropriate functions

## Spec Documentation

- Tasks: @.agent-os/specs/2025-09-02-cross-platform-shell-support/tasks.md
- Technical Specification: @.agent-os/specs/2025-09-02-cross-platform-shell-support/sub-specs/technical-spec.md