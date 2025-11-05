# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-05

### Added
- **Initial release** of Linebreaker - intelligent line breaking for Markdown and text files
- **Command-line interface** (`linebreaker` command) for processing files and directories
- **Python API** with `format_line()` and `break_text()` functions
- **Smart citation masking** - prevents `[@...]` citations from triggering unwanted line breaks
- **Decimal number masking** - protects numbers like `0.85` from being split
- **Hard breaks** on sentence boundaries (`.`, `?`, `!`) with intelligent abbreviation detection
- **Medium breaks** on colons and semicolons for long sentences (>80 characters)
- **Soft breaks** on conjunctions, commas, and logical operators for improved readability
- **YAML header preservation** - maintains frontmatter in Markdown files
- **Code block protection** - prevents line breaking inside code blocks
- **Comprehensive test suite** with 29 test cases
- **Pixi integration** for modern Python dependency management
- **GitHub Actions CI/CD** with automated testing and PyPI publishing
- **MIT License**

### Features
- **Hard Breaks (Sentence Boundaries)**:
  - Splits on `.`, `?`, `!` when both sides have 20+ characters
  - Recognizes common abbreviations: vs., Dr., Prof., Mr., Mrs., Ms., Ph.D., M.D., Jr., Sr., i.e., et al., vol., no., pp., fig.

- **Medium Breaks (Colons/Semicolons)**:
  - Splits sentences longer than 80 characters at `:` or `;`
  - Only when both parts have 20+ characters

- **Soft Breaks (Conjunctions)**:
  - Applied when there are 3+ sentences or sentence is >60 characters
  - Breaks on: `but`, `such as`, `for example`, `e.g.`, `i.e.` (after 20 chars)
  - Breaks on commas (after 40 chars)
  - Breaks on `and`, `or` (after 40 chars)

- **Smart Masking**:
  - Citations `[@...]` are masked to prevent internal dots from triggering breaks
  - Decimal numbers like `0.85` are masked similarly

### Technical Details
- **Python 3.8+** compatibility
- **Zero external dependencies** (uses only Python standard library)
- **Modern packaging** with `pyproject.toml`
- **Source distribution** and wheel builds
- **Comprehensive documentation** in README.md

### Infrastructure
- **GitHub Actions** for CI/CD
- **Automated PyPI publishing** on releases
- **Code coverage** reporting with Codecov
- **Pixi** for dependency management and environment handling

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities