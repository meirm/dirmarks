# Technical Stack

> Last Updated: 2025-09-02
> Version: 1.0.0

## Application Framework

- **Framework:** Python
- **Version:** 3.9+
- **Rationale:** Cross-platform compatibility, rich standard library, excellent CLI tooling ecosystem

## Package Management & Build

- **Build System:** Poetry
- **Version:** Latest stable
- **Rationale:** Modern dependency management, packaging, and publishing workflow

## Distribution & Installation

- **Primary Distribution:** PyPI (pip)
- **Installation Method:** `pip install dirmarks`
- **Rationale:** Standard Python package distribution, familiar to target users

## Shell Integration

- **Supported Shells:** Bash, Zsh
- **Integration Method:** Function generation and sourcing
- **Configuration:** Shell-specific function files

## Storage & Persistence

- **Data Format:** JSON
- **Storage Location:** User home directory (`~/.dirmarks/`)
- **Backup Strategy:** File-based with import/export capability

## Development Tools

- **Testing Framework:** pytest
- **Code Quality:** pylint, black (code formatting)
- **CI/CD:** GitHub Actions
- **Version Control:** Git

## Deployment Architecture

- **Distribution:** Single Python package
- **Installation:** User-space via pip
- **Shell Integration:** Post-install shell function setup
- **Updates:** Standard pip upgrade workflow