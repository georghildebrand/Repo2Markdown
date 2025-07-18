# repo2md

A minimal Python CLI tool that exports Git repository contents to structured Markdown files. Perfect for creating comprehensive repository documentation, code reviews, or feeding codebases to AI tools.

## Features

- **Git Integration**: Automatically scans Git-tracked files using `git ls-files`
- **Smart Filtering**: Respects `.gitignore` patterns and excludes binary files
- **Language Detection**: Automatically detects 25+ programming languages for syntax highlighting
- **Multiple Output Options**: File, clipboard, or stdout (combinable)
- **Configurable Filtering**: Custom ignore patterns, file size limits, meta file handling
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Minimal Dependencies**: Only uses Python stdlib + `pyperclip` for clipboard functionality

## Todo

[] Make pip package
[] Cleanup and remove clutter
[] Scan Todos in code

## Installation

### From Source

```bash
pip install git+https://github.com/georghildebrand/Repo2Markdown.git@main
```

Or from local clone:

```bash
git clone https://github.com/georghildebrand/Repo2Markdown.git
cd Repo2Markdown
make install
```

### Development Setup
```bash
# Full development environment
make dev-setup

# Or manually
poetry install --with dev
poetry shell
```

### Build and Install Wheel
```bash
make install-wheel
```

## Quick Start

```bash
# Export current directory to stdout
repo2md .

# Export to a file
repo2md . --output my-repo.md

# Copy to clipboard
repo2md . --clipboard

# Exclude README, LICENSE, etc.
repo2md . --exclude-meta-files

# Combine outputs
repo2md . --output docs.md --clipboard
```

## Usage

```
repo2md [PATH] [OPTIONS]

Arguments:
  PATH                  Path to repository (default: current directory)

Output Options:
  --output, -o PATH     Write to file
  --clipboard, -c       Copy to clipboard
  --stdout, -s          Output to stdout (default)

Debugging Options:
  -v, --verbose         Show lists of all files included and all files ignored (printed to stderr for debugging)

Filtering Options:
  --ignore PATTERN      Additional ignore patterns (repeatable)
  --exclude-meta-files  Exclude README, LICENSE, .gitignore, etc.
  --max-file-size SIZE  Maximum file size in bytes (default: 1MB)
  --include-meta FILES  Include specific meta files
  --exclude-meta FILES  Exclude specific meta files
```

## Examples

### Basic Export
```bash
# Export current repository
repo2md .

# Export specific directory
repo2md ./my-project

# Export with custom output path
repo2md . --output repository-export.md
```

### Output Options
```bash
# Copy to clipboard for pasting elsewhere
repo2md . --clipboard

# Both file and clipboard
repo2md . --output backup.md --clipboard

# Output to stdout for piping
repo2md . --stdout | less
```

### Advanced Filtering
```bash
# Exclude meta files (README, LICENSE, etc.)
repo2md . --exclude-meta-files

# Custom ignore patterns
repo2md . --ignore "*.log" --ignore "temp/*" --ignore "*.tmp"

# Limit file size (500KB max)
repo2md . --max-file-size 500000

# Include only specific files, ignore others
repo2md . --exclude-meta-files --include-meta README.md

# Complex filtering for AI tools
repo2md . --exclude-meta-files --ignore "*.test.js" --ignore "dist/*" --max-file-size 100000 --clipboard

# Debug what files are included/ignored
repo2md . --verbose --ignore "*.log" --exclude-meta-files
```

## Output Format

The generated Markdown includes:

1. **Repository Summary**: File count, total size, root path
2. **File Structure**: Directory tree organized by folders
3. **File Contents**: Each file with syntax highlighting and metadata

Example output structure:
```markdown
# MyProject

## Repository Summary
- **Files:** 15
- **Total Size:** 0.25 MB
- **Repository Root:** `/path/to/MyProject`

## File Structure

### Root Directory
- main.py
- requirements.txt

### src/
- __init__.py
- core.py

## File Contents

### main.py
**Size:** 1024 bytes
**Language:** python

```python
def main():
    print("Hello World")
```

## Development

This project uses **Poetry** for dependency management and **Make** for build automation:

### Quick Development Commands

```bash
# Setup development environment
make dev-setup              # Install deps + setup pre-commit hooks

# Daily development
make install                 # Install/update dependencies
make format                  # Format code with Black
make lint                    # Run flake8 + mypy
make test                    # Run tests
make test-cov                # Run tests with coverage

# Quality assurance
make all-checks              # Run format-check + lint + test
make ci-local                # Full CI pipeline simulation

# Building and packaging
make build                   # Build wheel + source dist
make install-wheel           # Build and install wheel locally
make clean                   # Clean build artifacts

# Tool execution
make run                     # Run tool on current directory
make run-example             # Generate example_output.md
make run-help                # Show CLI help
```

### Testing Commands

```bash
# Run specific test files
poetry run pytest tests/test_core.py -v
poetry run pytest tests/test_cli.py -v

# Test with coverage and HTML report
make test-cov

# Integration testing
make run-example
poetry run repo2md --help
```

### Code Quality

```bash
# Check formatting (without changing files)
make format-check

# Format code
make format

# Run linting
make lint

# Run all quality checks
make all-checks
```

## Supported Languages

The tool automatically detects and provides syntax highlighting for:

**Programming Languages:** Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala

**Web Technologies:** HTML, CSS, SCSS/Sass, JSX, TSX

**Data/Config:** JSON, YAML, TOML, XML, SQL, INI

**Scripts/Shell:** Bash, Zsh, Fish, PowerShell

**Documentation:** Markdown, Text

**Special Files:** Dockerfile, Makefile, .gitignore

## Architecture

The tool follows a clean, modular design based on C4 architecture principles:

### System Overview
- **Core Module**: Repository scanning, filtering, and Markdown generation
- **CLI Module**: Command-line interface and argument handling
- **Output Module**: File, clipboard, and stdout output handling

### Key Design Decisions
- **Minimal Dependencies**: Only `pyperclip` for clipboard functionality
- **Standard Library Focus**: Uses `subprocess`, `fnmatch`, `argparse` instead of heavy dependencies
- **Git Integration**: Leverages `git ls-files` for accurate file discovery
- **Binary File Detection**: Automatically excludes binary files from output

### Architecture Diagrams

The system architecture is documented using C4 diagrams:

#### System Context Diagram
![System Context Diagram](docs/architecture/images/C4_Level1_repo2md.png)

*High-level system interactions showing how developers use the repo2md CLI tool.*

#### Container Diagram
![Container Diagram](docs/architecture/images/C4_Level2_repo2md.png)

*Internal system structure showing the CLI, Core, and Output modules.*

#### Component Diagram
![Component Diagram](docs/architecture/images/C4_Level3_repo2md.png)

*Detailed component breakdown of the Core module's internal structure.*

> **📝 Note:** These diagrams are automatically generated from the PlantUML source files in `docs/architecture/c4/` and updated by our CI/CD pipeline.
>
> **🔧 Local Rendering:** Use the [PlantUML VS Code extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) or [online PlantUML server](http://www.plantuml.com/plantuml/uml/) to view/edit the source diagrams.

### Rendering Diagrams Locally

```bash
# Install PlantUML (macOS)
brew install plantuml

# Install PlantUML (Ubuntu/Debian)
sudo apt-get install plantuml

# Render diagrams to PNG
make render-diagrams

# Generate all documentation
make docs
```

## Requirements

- **Python 3.11+** (uses modern type hints)
- **Git** (for repository scanning)
- **Poetry** (for dependency management)
- **pyperclip** (for clipboard functionality - automatically installed)

## Performance

- **Fast scanning**: Leverages Git for efficient file discovery
- **Memory efficient**: Processes files individually, not all in memory
- **Smart filtering**: Multiple layers of filtering reduce processing overhead
- **Binary detection**: Quick binary file detection prevents unnecessary processing

Typical performance:
- Small projects (< 100 files): < 1 second
- Medium projects (100-1000 files): 1-5 seconds
- Large projects (1000+ files): 5-30 seconds (depending on file sizes and filtering)

## Troubleshooting

### Common Issues

**"Git not found" or empty output:**
```bash
# Make sure you're in a Git repository
git status

# Or scan directory without Git integration
repo2md . --ignore ".git/*"
```

**"Pyperclip not available" error:**
```bash
# Install clipboard support
make install
# or
poetry install --with dev
```

**Large output files:**
```bash
# Reduce file size with filtering
repo2md . --exclude-meta-files --max-file-size 50000 --ignore "*.log" --ignore "dist/*"
```

**Development environment issues:**
```bash
# Reset development environment
make clean
make dev-setup

# Check dependencies
poetry check
poetry show --tree
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Set up development environment: `make dev-setup`
4. Make your changes with tests
5. Run quality checks: `make all-checks`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Submit a pull request

### Development Workflow

The project uses **Makefile-based workflows** for both local development and CI/CD:

- **Local Development**: All commands use `make` targets for consistency
- **GitHub Actions**: CI workflows use the same `make` targets
- **No Discrepancy**: What runs locally is exactly what runs in CI

#### CI/CD Pipeline

- **CI Pipeline** (`make ci-local`): Runs on every push and PR
  - Tests on Python 3.11 and 3.12
  - Code formatting and linting checks (`make all-checks`)
  - Cross-platform integration tests (Ubuntu, Windows, macOS)
  - Security scanning with safety and bandit
  - Coverage reporting

- **Documentation** (`make docs`): Auto-updates on doc changes
  - Renders PlantUML diagrams to PNG (`make render-diagrams`)
  - Validates markdown links
  - Workflow validation (`make validate-workflows`)

- **Release Pipeline**: Triggered on version tags
  - Publishes to PyPI automatically
  - Creates GitHub releases with changelog
  - Includes build artifacts

### Available Make Targets

```bash
make help                    # Show all available commands
make install                 # Install dependencies
make install-dev             # Development installation
make install-wheel           # Build and install wheel
make test                    # Run tests
make test-cov                # Run tests with coverage
make lint                    # Run linting (flake8 + mypy)
make format                  # Format code with Black
make format-check            # Check formatting without changes
make all-checks              # Run format-check + lint + test
make clean                   # Clean build artifacts
make build                   # Build package
make run                     # Run CLI on current directory
make run-help                # Show CLI help
make run-example             # Generate example output
make dev-setup               # Set up development environment
make render-diagrams         # Render PlantUML diagrams
make docs                    # Generate all documentation
make validate-workflows      # Validate GitHub Actions
make ci-local                # Run complete CI pipeline locally
make all                     # Run everything (format, lint, test, docs, build)
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [GitHub's repository export tools](https://docs.github.com/en/repositories)
- [Tree command](https://en.wikipedia.org/wiki/Tree_(command)) for directory visualization
- [Sourcegraph](https://sourcegraph.com/) for code search and navigation
- [DocToc](https://github.com/thlorenz/doctoc) for table of contents generation

## Changelog

### v0.1.0 (Current)
- Initial release with Poetry-based dependency management
- Core repository scanning functionality
- Markdown export with syntax highlighting
- Multiple output options (file, clipboard, stdout)
- Smart filtering with .gitignore integration
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive test suite with coverage reporting
- Makefile-based development workflow
- GitHub Actions CI/CD pipeline
- Architecture documentation with C4 diagrams
