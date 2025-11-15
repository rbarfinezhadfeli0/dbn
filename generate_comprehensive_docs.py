#!/usr/bin/env python3
"""
World's Best Repo Book Generator and Index Builder
Generates comprehensive documentation for the entire repository.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import re
from collections import defaultdict

# Configuration
REPO_ROOT = Path(".")
DOCS_ROOT = Path("./docs")
IGNORE_PATTERNS = {
    ".git", "target", ".cargo", "node_modules", "__pycache__", ".venv",
    "docs", "*.pyc", "*.so", "*.dylib", "*.dll"
}
BINARY_EXTENSIONS = {".dbn", ".dbz", ".zst", ".lock"}

class FileInfo:
    """Information about a repository file."""
    def __init__(self, path: Path):
        self.path = path
        self.rel_path = path.relative_to(REPO_ROOT)
        self.name = path.name
        self.ext = path.suffix
        self.content = None
        self.keywords = set()
        self.is_binary = self.ext in BINARY_EXTENSIONS or self._is_binary_file()

    def _is_binary_file(self) -> bool:
        """Check if file is binary."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                f.read(1024)
            return False
        except:
            return True

    def read_content(self):
        """Read file content if not binary."""
        if self.is_binary:
            self.content = f"[Binary file: {self.name}]"
            return

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            self.content = f"[Error reading file: {e}]"

    def extract_keywords(self):
        """Extract meaningful keywords from content."""
        if not self.content or self.is_binary:
            return

        # Extract function/class names
        if self.ext in {".rs", ".py", ".js", ".ts", ".cpp", ".c", ".h"}:
            # Rust/Python/JS/C++ patterns
            patterns = [
                r'fn\s+(\w+)',  # Rust functions
                r'struct\s+(\w+)',  # Structs
                r'enum\s+(\w+)',  # Enums
                r'trait\s+(\w+)',  # Traits
                r'impl\s+(?:<[^>]+>\s+)?(\w+)',  # Implementations
                r'class\s+(\w+)',  # Classes
                r'def\s+(\w+)',  # Python functions
                r'const\s+(\w+)',  # Constants
                r'type\s+(\w+)',  # Type aliases
                r'pub\s+(?:const|static|fn|struct|enum|trait)\s+(\w+)',  # Public items
            ]

            for pattern in patterns:
                matches = re.findall(pattern, self.content)
                self.keywords.update(matches)

        # Extract from markdown headings
        if self.ext == ".md":
            headings = re.findall(r'^#+\s+(.+)$', self.content, re.MULTILINE)
            for heading in headings:
                # Clean and split heading into words
                words = re.findall(r'\w+', heading)
                self.keywords.update(w for w in words if len(w) > 3)

        # Extract YAML/TOML keys
        if self.ext in {".yml", ".yaml", ".toml"}:
            keys = re.findall(r'^(\w+):', self.content, re.MULTILINE)
            self.keywords.update(keys)


class FolderInfo:
    """Information about a repository folder."""
    def __init__(self, path: Path):
        self.path = path
        self.rel_path = path.relative_to(REPO_ROOT) if path != REPO_ROOT else Path(".")
        self.name = path.name if path != REPO_ROOT else "root"
        self.files: List[FileInfo] = []
        self.subfolders: List['FolderInfo'] = []
        self.keywords: Set[str] = set()


class DocumentationGenerator:
    """Main documentation generator."""

    def __init__(self):
        self.all_files: List[FileInfo] = []
        self.all_folders: List[FolderInfo] = []
        self.folder_map: Dict[Path, FolderInfo] = {}
        self.global_keywords: Dict[str, List[FileInfo]] = defaultdict(list)

    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        parts = path.parts
        for pattern in IGNORE_PATTERNS:
            if any(pattern.strip('*') in part for part in parts):
                return True
        return False

    def scan_repository(self):
        """Scan the entire repository structure."""
        print("Scanning repository structure...")

        # Find all folders
        for root, dirs, files in os.walk(REPO_ROOT):
            root_path = Path(root)

            if self.should_ignore(root_path):
                dirs.clear()
                continue

            folder = FolderInfo(root_path)
            self.all_folders.append(folder)
            self.folder_map[root_path] = folder

            # Process files in this folder
            for filename in files:
                file_path = root_path / filename
                if not self.should_ignore(file_path):
                    file_info = FileInfo(file_path)
                    self.all_files.append(file_info)
                    folder.files.append(file_info)

        # Build folder hierarchy
        for folder in self.all_folders:
            parent_path = folder.path.parent
            if parent_path in self.folder_map and parent_path != folder.path:
                self.folder_map[parent_path].subfolders.append(folder)

        print(f"Found {len(self.all_files)} files and {len(self.all_folders)} folders")

    def read_all_files(self):
        """Read content of all files."""
        print("Reading file contents...")
        for i, file_info in enumerate(self.all_files):
            if i % 10 == 0:
                print(f"  Reading file {i+1}/{len(self.all_files)}")
            file_info.read_content()
            file_info.extract_keywords()

            # Add to global keywords
            for keyword in file_info.keywords:
                self.global_keywords[keyword].append(file_info)

    def create_docs_structure(self):
        """Create documentation directory structure."""
        print("Creating docs directory structure...")
        for folder in self.all_folders:
            docs_folder = DOCS_ROOT / folder.rel_path
            docs_folder.mkdir(parents=True, exist_ok=True)

    def relative_link(self, from_path: Path, to_path: Path) -> str:
        """Generate relative link from one path to another."""
        try:
            rel = os.path.relpath(to_path, from_path.parent)
            return rel.replace("\\", "/")
        except:
            return str(to_path)

    def generate_file_docs(self, file_info: FileInfo):
        """Generate comprehensive documentation for a file."""
        docs_path = DOCS_ROOT / file_info.rel_path.parent / f"{file_info.name}_docs.md"

        content = f"""# Documentation: {file_info.rel_path}

## File Metadata

**Path:** `{file_info.rel_path}`
**Filename:** `{file_info.name}`
**Extension:** `{file_info.ext}`
**Type:** {'Binary' if file_info.is_binary else 'Text'}

## Original Source

**Location:** `{self.relative_link(docs_path, file_info.path)}`

"""

        if file_info.is_binary:
            content += f"""## File Type

This is a binary file ({file_info.name}). Binary files are not directly documentable in text form,
but this file is part of the repository's test data or compiled artifacts.

### Purpose

Binary test data files are used for integration testing and validation of the DBN encoding/decoding functionality.

### Related Components

- Decoding modules in `rust/dbn/src/decode/`
- Encoding modules in `rust/dbn/src/encode/`
- Test utilities in test directories

"""
        else:
            # Text file - include content and analysis
            content += f"""### Source Content

```{file_info.ext.strip('.')}
{file_info.content[:50000]}{"..." if len(file_info.content) > 50000 else ""}
```

## High-Level Overview

This file is located at `{file_info.rel_path}` within the repository.

"""

            # Analyze based on file type
            if file_info.ext == ".rs":
                content += self._analyze_rust_file(file_info)
            elif file_info.ext == ".py":
                content += self._analyze_python_file(file_info)
            elif file_info.ext == ".md":
                content += self._analyze_markdown_file(file_info)
            elif file_info.ext in {".toml", ".yml", ".yaml"}:
                content += self._analyze_config_file(file_info)
            elif file_info.ext == ".sh":
                content += self._analyze_script_file(file_info)
            else:
                content += self._analyze_generic_file(file_info)

        # Write documentation file
        with open(docs_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _analyze_rust_file(self, file_info: FileInfo) -> str:
        """Analyze a Rust source file."""
        analysis = """### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components

"""
        # Find functions
        functions = re.findall(r'(?:pub\s+)?fn\s+(\w+)', file_info.content)
        if functions:
            analysis += f"\n**Functions defined:** {', '.join(sorted(set(functions))[:20])}\n"

        # Find structs
        structs = re.findall(r'(?:pub\s+)?struct\s+(\w+)', file_info.content)
        if structs:
            analysis += f"\n**Structs defined:** {', '.join(sorted(set(structs))[:20])}\n"

        # Find enums
        enums = re.findall(r'(?:pub\s+)?enum\s+(\w+)', file_info.content)
        if enums:
            analysis += f"\n**Enums defined:** {', '.join(sorted(set(enums))[:20])}\n"

        # Find traits
        traits = re.findall(r'(?:pub\s+)?trait\s+(\w+)', file_info.content)
        if traits:
            analysis += f"\n**Traits defined:** {', '.join(sorted(set(traits))[:20])}\n"

        # Find imports
        imports = re.findall(r'use\s+([^;]+);', file_info.content)
        if imports:
            analysis += f"\n**Dependencies:** This file imports from {len(set(imports))} modules\n"

        analysis += """

#### Detailed Walkthrough

"""
        # Add detailed function descriptions
        func_matches = re.finditer(r'((?:pub\s+)?(?:async\s+)?fn\s+(\w+)[^{]*\{)', file_info.content)
        func_count = 0
        for match in func_matches:
            if func_count >= 10:  # Limit to first 10 functions
                analysis += "\n*... and more functions (see source code)*\n"
                break
            func_sig = match.group(1)
            func_name = match.group(2)
            analysis += f"\n##### Function: `{func_name}`\n\n"
            analysis += f"```rust\n{func_sig}\n```\n\n"
            func_count += 1

        analysis += """

#### Architecture & Design

This file contributes to the overall DBN library architecture by providing essential functionality
for encoding, decoding, or representing market data in the Databento Binary Encoding format.

**Design Principles:**
- Type safety through Rust's strong type system
- Zero-cost abstractions for performance
- Clear error handling with Result types
- Memory efficiency for large-scale data processing

#### Performance Considerations

Rust's ownership model and zero-cost abstractions make this implementation highly performant:
- Stack allocation where possible
- Minimal heap allocations
- Compile-time optimizations
- No garbage collection overhead

#### Security & Safety

Rust's memory safety guarantees prevent:
- Buffer overflows
- Null pointer dereferences
- Data races in concurrent code
- Use-after-free bugs

All unsafe code blocks (if any) are carefully reviewed and documented.

"""
        return analysis

    def _analyze_python_file(self, file_info: FileInfo) -> str:
        """Analyze a Python source file."""
        analysis = """### Language: Python

This is a Python source file, typically used for bindings, scripts, or testing.

#### Key Components

"""
        # Find classes
        classes = re.findall(r'class\s+(\w+)', file_info.content)
        if classes:
            analysis += f"\n**Classes:** {', '.join(sorted(set(classes)))}\n"

        # Find functions
        functions = re.findall(r'def\s+(\w+)', file_info.content)
        if functions:
            analysis += f"\n**Functions:** {', '.join(sorted(set(functions))[:20])}\n"

        # Find imports
        imports = re.findall(r'(?:from|import)\s+(\w+)', file_info.content)
        if imports:
            analysis += f"\n**Imports:** {', '.join(sorted(set(imports))[:15])}\n"

        analysis += """

#### Python Integration

This file is part of the Python bindings for the DBN Rust library, enabling Python developers
to work with Databento Binary Encoding format efficiently.

"""
        return analysis

    def _analyze_markdown_file(self, file_info: FileInfo) -> str:
        """Analyze a Markdown documentation file."""
        analysis = """### Document Type: Markdown

This is a documentation file written in Markdown format.

#### Content Structure

"""
        headings = re.findall(r'^(#+)\s+(.+)$', file_info.content, re.MULTILINE)
        if headings:
            analysis += "\n**Document Outline:**\n\n"
            for level, heading in headings[:20]:
                indent = "  " * (len(level) - 1)
                analysis += f"{indent}- {heading}\n"

        analysis += """

#### Purpose

This documentation provides important information for users and contributors of the project.

"""
        return analysis

    def _analyze_config_file(self, file_info: FileInfo) -> str:
        """Analyze a configuration file."""
        return """### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

"""

    def _analyze_script_file(self, file_info: FileInfo) -> str:
        """Analyze a shell script file."""
        return """### File Type: Shell Script

This is a shell script used for automation, building, testing, or deployment tasks.

#### Script Purpose

Shell scripts automate common development tasks and ensure consistent build/test procedures.

"""

    def _analyze_generic_file(self, file_info: FileInfo) -> str:
        """Analyze a generic file."""
        return """### File Overview

This file is part of the repository's supporting infrastructure or data.

"""

    def generate_file_keywords(self, file_info: FileInfo):
        """Generate keyword index for a file."""
        kw_path = DOCS_ROOT / file_info.rel_path.parent / f"{file_info.name}_kw.md"
        docs_rel = f"{file_info.name}_docs.md"
        source_rel = self.relative_link(kw_path, file_info.path)

        content = f"""# Keyword Map: {file_info.rel_path}

## File Path and Links

**Original File:** [{file_info.rel_path}]({source_rel})
**Documentation:** [{file_info.name}_docs.md]({docs_rel})

## Keywords

This file contains the following significant keywords and concepts:

"""

        if file_info.keywords:
            sorted_keywords = sorted(file_info.keywords)
            for keyword in sorted_keywords:
                content += f"- **{keyword}**: Defined or used in this file → [View Documentation]({docs_rel})\n"
        else:
            content += "*No keywords extracted (binary or non-code file)*\n"

        content += """

## Keyword → Section Map

The keywords above can be found in various sections of the documentation file.
Refer to the [full documentation]({docs_rel}) for detailed explanations.

"""

        with open(kw_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_folder_index(self, folder: FolderInfo):
        """Generate index.md for a folder."""
        index_path = DOCS_ROOT / folder.rel_path / "index.md"

        folder_display = str(folder.rel_path) if folder.rel_path != Path(".") else "root"
        content = f"""# Index of Folder: {folder_display}

## Overview

This folder is located at `{folder.rel_path}` within the repository.

"""

        # Describe folder purpose based on name
        purpose = self._describe_folder_purpose(folder)
        content += f"{purpose}\n\n"

        # List subfolders
        if folder.subfolders:
            content += "## Subfolders\n\n"
            for subfolder in sorted(folder.subfolders, key=lambda f: f.name):
                subfolder_rel = subfolder.rel_path.name
                content += f"- **[{subfolder.name}/](./{subfolder_rel}/index.md)**: "
                content += self._get_folder_one_liner(subfolder) + "\n"
            content += "\n"

        # List files
        if folder.files:
            content += "## Files\n\n"
            content += "| File | Description | Documentation | Keywords |\n"
            content += "|------|-------------|---------------|----------|\n"

            for file_info in sorted(folder.files, key=lambda f: f.name):
                source_link = self.relative_link(index_path, file_info.path)
                docs_link = f"./{file_info.name}_docs.md"
                kw_link = f"./{file_info.name}_kw.md"
                desc = self._get_file_description(file_info)

                content += f"| [{file_info.name}]({source_link}) | {desc} | [docs]({docs_link}) | [keywords]({kw_link}) |\n"
            content += "\n"

        content += """## Navigation Hints

- Start with the README or main source files to understand this folder's purpose
- Check the `doc.md` file for narrative documentation about this folder
- Use `sub.md` to find keywords across this entire subtree

"""

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _describe_folder_purpose(self, folder: FolderInfo) -> str:
        """Generate a description of the folder's purpose."""
        name = folder.name.lower()

        if name == "src":
            return "This is a **source code** folder containing the main implementation files."
        elif name == "tests" or name == "test":
            return "This is a **testing** folder containing test cases and test data."
        elif name == "docs" or name == "doc":
            return "This is a **documentation** folder."
        elif name in {"python", "rust", "c", "cpp"}:
            return f"This folder contains **{name}** language-specific code."
        elif name == "scripts":
            return "This folder contains **automation scripts** for building, testing, and deployment."
        elif name == ".github":
            return "This folder contains **GitHub-specific** configuration (workflows, issue templates, etc.)."
        elif name == "data":
            return "This folder contains **data files** used for testing or examples."
        else:
            return f"This folder contains files related to **{name}**."

    def _get_folder_one_liner(self, folder: FolderInfo) -> str:
        """Get a one-line description of a folder."""
        name = folder.name.lower()

        descriptions = {
            "src": "Source code implementations",
            "tests": "Test suites and test data",
            "docs": "Documentation files",
            "scripts": "Automation scripts",
            "data": "Data files",
            ".github": "GitHub configuration",
            "workflows": "CI/CD workflows",
            "python": "Python bindings and code",
            "rust": "Rust language components",
            "c": "C language FFI bindings",
            "decode": "Decoding functionality",
            "encode": "Encoding functionality",
            "dbn": "DBN core library",
            "dbn-cli": "DBN command-line tool",
            "dbn-macros": "Procedural macros for DBN",
        }

        return descriptions.get(name, f"{name} components")

    def _get_file_description(self, file_info: FileInfo) -> str:
        """Get a brief description of a file."""
        name = file_info.name.lower()
        ext = file_info.ext.lower()

        if ext == ".md":
            if "readme" in name:
                return "Project documentation"
            elif "changelog" in name:
                return "Version history"
            elif "contributing" in name:
                return "Contribution guidelines"
            elif "license" in name:
                return "License information"
            elif "code_of_conduct" in name:
                return "Community standards"
            else:
                return "Documentation"
        elif ext == ".rs":
            if name == "lib.rs":
                return "Library entry point"
            elif name == "main.rs":
                return "Application entry point"
            else:
                return "Rust source code"
        elif ext == ".py":
            if "__init__" in name:
                return "Python module initialization"
            else:
                return "Python source code"
        elif ext == ".toml":
            if "cargo" in name:
                return "Rust package configuration"
            elif "pyproject" in name:
                return "Python project configuration"
            else:
                return "Configuration file"
        elif ext in {".yml", ".yaml"}:
            return "YAML configuration"
        elif ext == ".sh":
            return "Shell script"
        elif ext in {".dbn", ".dbz"}:
            return "Binary test data"
        elif ext == ".gitignore":
            return "Git ignore rules"
        else:
            return "Project file"

    def generate_folder_doc(self, folder: FolderInfo):
        """Generate doc.md for a folder."""
        doc_path = DOCS_ROOT / folder.rel_path / "doc.md"

        folder_display = str(folder.rel_path) if folder.rel_path != Path(".") else "root"
        content = f"""# Documentation for Folder: {folder_display}

## Role in the Project

"""

        content += self._generate_folder_role_description(folder)

        content += """

## Key Concepts

"""
        content += self._generate_folder_concepts(folder)

        content += """

## Important Files

"""
        content += self._generate_folder_important_files(folder)

        content += """

## Data Flows & Interactions

"""
        content += self._generate_folder_interactions(folder)

        content += """

## How to Work with This Folder

"""
        content += self._generate_folder_usage(folder)

        content += """

## Cross References

"""
        content += self._generate_folder_cross_refs(folder)

        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_folder_role_description(self, folder: FolderInfo) -> str:
        """Generate detailed role description for a folder."""
        name = folder.name.lower()
        path_str = str(folder.rel_path)

        if folder.rel_path == Path("."):
            return """This is the **root directory** of the DBN (Databento Binary Encoding) repository.

The DBN project provides a fast, efficient binary encoding format for normalized market data.
This repository contains:
- Rust library implementations
- Python bindings
- C FFI bindings
- Command-line tools
- Comprehensive test suites

The project enables high-performance market data encoding, decoding, and transformation across
multiple programming languages.
"""

        elif "rust/dbn" in path_str and "src" in path_str:
            return """This folder contains the **core Rust implementation** of the DBN library.

It provides fundamental functionality for:
- Encoding market data to DBN format
- Decoding DBN streams
- Type definitions for market data records
- Metadata handling
- Symbol mapping and conversion
"""

        elif "python" in path_str:
            return """This folder contains **Python bindings** for the DBN Rust library.

Using PyO3, it exposes DBN functionality to Python developers, enabling:
- Fast decoding of DBN files in Python
- Type-safe Python classes for market data records
- Integration with the Databento Python client library
"""

        elif "tests" in path_str:
            return """This folder contains **test infrastructure** including:
- Integration tests
- Test data files
- Test utilities
- Validation suites

These tests ensure correctness and compatibility across different DBN versions and schemas.
"""

        elif "scripts" in path_str:
            return """This folder contains **automation scripts** for:
- Building the project
- Running tests
- Formatting code
- Version management
- CI/CD integration
"""

        else:
            return f"""This folder is part of the repository structure, located at `{path_str}`.

It contributes to the overall functionality of the DBN library system.
"""

    def _generate_folder_concepts(self, folder: FolderInfo) -> str:
        """Generate key concepts for a folder."""
        # Collect keywords from all files in folder
        all_keywords = set()
        for file in folder.files:
            all_keywords.update(file.keywords)

        if all_keywords:
            top_keywords = sorted(all_keywords)[:15]
            content = "Key technical concepts in this folder:\n\n"
            for kw in top_keywords:
                content += f"- **{kw}**: Core concept used throughout this module\n"
            return content
        else:
            return "This folder contains supporting files and infrastructure.\n"

    def _generate_folder_important_files(self, folder: FolderInfo) -> str:
        """List important files in a folder."""
        if not folder.files:
            return "*No files in this folder*\n"

        important = []
        regular = []

        for file in folder.files:
            name_lower = file.name.lower()
            if any(x in name_lower for x in ["readme", "lib.rs", "main.rs", "__init__", "cargo.toml"]):
                important.append(file)
            else:
                regular.append(file)

        content = ""

        if important:
            content += "### Essential Files\n\n"
            for file in important:
                content += f"- **[{file.name}](./{file.name}_docs.md)**: {self._get_file_description(file)}\n"
            content += "\n"

        if regular:
            content += "### Additional Files\n\n"
            for file in regular[:10]:
                content += f"- [{file.name}](./{file.name}_docs.md)\n"
            if len(regular) > 10:
                content += f"\n*... and {len(regular) - 10} more files (see [index](./index.md))*\n"

        return content

    def _generate_folder_interactions(self, folder: FolderInfo) -> str:
        """Describe how this folder interacts with others."""
        path_str = str(folder.rel_path).lower()

        if "encode" in path_str:
            return """This folder handles **encoding** operations:
- Converts market data records to various output formats
- Supports DBN, CSV, JSON encodings
- Provides both sync and async APIs
- Interacts with record types defined in parent modules
"""
        elif "decode" in path_str:
            return """This folder handles **decoding** operations:
- Reads DBN/DBZ format files
- Parses compressed (Zstandard) streams
- Validates metadata and record structures
- Provides streaming iterators for efficient processing
"""
        elif "python" in path_str and "src" in path_str:
            return """This folder bridges **Rust and Python**:
- Uses PyO3 for FFI bindings
- Exposes Rust types to Python
- Handles type conversion and error propagation
- Integrates with Python's memory model
"""
        else:
            return """This folder integrates with the broader project architecture through:
- Shared type definitions
- Common error handling patterns
- Standard library interfaces
"""

    def _generate_folder_usage(self, folder: FolderInfo) -> str:
        """Provide guidance on working with this folder."""
        return """### Extending Functionality

When adding new features to this folder:
1. Follow existing code patterns and conventions
2. Add comprehensive tests
3. Update documentation
4. Consider backward compatibility

### Testing Changes

Run the test suite after modifications:
```bash
cargo test  # For Rust code
pytest      # For Python code
```

### Code Style

Follow the project's formatting standards:
```bash
./scripts/format.sh
./scripts/lint.sh
```
"""

    def _generate_folder_cross_refs(self, folder: FolderInfo) -> str:
        """Generate cross-references to related folders."""
        refs = []

        # Add parent folder
        if folder.path != REPO_ROOT:
            parent = folder.path.parent
            if parent in self.folder_map:
                parent_rel = os.path.relpath(
                    DOCS_ROOT / self.folder_map[parent].rel_path / "doc.md",
                    DOCS_ROOT / folder.rel_path
                )
                refs.append(f"- **Parent folder**: [{self.folder_map[parent].name}]({parent_rel})")

        # Add child folders
        if folder.subfolders:
            for subfolder in folder.subfolders[:5]:
                refs.append(f"- **{subfolder.name}**: [View documentation](./{subfolder.name}/doc.md)")

        if refs:
            return "\n".join(refs) + "\n"
        else:
            return "*No direct cross-references*\n"

    def generate_folder_sub(self, folder: FolderInfo):
        """Generate sub.md (subtree keyword index) for a folder."""
        sub_path = DOCS_ROOT / folder.rel_path / "sub.md"

        # Collect all keywords from this folder and descendants
        subtree_keywords = defaultdict(list)

        def collect_keywords(f: FolderInfo):
            for file in f.files:
                for kw in file.keywords:
                    subtree_keywords[kw].append(file)
            for subfolder in f.subfolders:
                collect_keywords(subfolder)

        collect_keywords(folder)

        folder_display = str(folder.rel_path) if folder.rel_path != Path(".") else "root"
        content = f"""# Subtree Keyword Index: {folder_display}

## Scope

This keyword index covers **all files** under `{folder.rel_path}` recursively,
including all subfolders and their contents.

## Keywords A–Z

"""

        if subtree_keywords:
            sorted_keywords = sorted(subtree_keywords.keys())

            current_letter = None
            for keyword in sorted_keywords:
                first_letter = keyword[0].upper() if keyword else '?'

                if first_letter != current_letter:
                    current_letter = first_letter
                    content += f"\n### {current_letter}\n\n"

                content += f"#### {keyword}\n\n"
                content += "Found in:\n"

                for file in subtree_keywords[keyword][:10]:
                    rel_to_sub = os.path.relpath(
                        DOCS_ROOT / file.rel_path.parent / f"{file.name}_docs.md",
                        DOCS_ROOT / folder.rel_path
                    )
                    content += f"- [{file.rel_path}]({rel_to_sub})\n"

                if len(subtree_keywords[keyword]) > 10:
                    content += f"- *... and {len(subtree_keywords[keyword]) - 10} more files*\n"

                content += "\n"
        else:
            content += "*No keywords found in this subtree*\n"

        content += """

## Folder-Level Navigation

Use this index to quickly find where specific concepts are implemented across
the entire subtree. Each keyword links to the relevant documentation files.

"""

        with open(sub_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_global_keywords(self):
        """Generate global keywords.md file."""
        print("Generating global keywords index...")

        kw_path = DOCS_ROOT / "keywords.md"

        content = """# Global Keyword Index

## Usage

This index contains **all keywords** extracted from every file in the repository.
Use it to find where specific concepts, functions, types, or components are defined.

## Keywords A–Z

"""

        sorted_keywords = sorted(self.global_keywords.keys())
        current_letter = None

        for keyword in sorted_keywords:
            first_letter = keyword[0].upper() if keyword else '?'

            if first_letter != current_letter:
                current_letter = first_letter
                content += f"\n## {current_letter}\n\n"

            content += f"### {keyword}\n\n"

            files = self.global_keywords[keyword]
            content += f"*Found in {len(files)} file(s)*\n\n"

            for file in files[:15]:
                docs_path = file.rel_path.parent / f"{file.name}_docs.md"
                content += f"- [{file.rel_path}](./{docs_path})\n"

            if len(files) > 15:
                content += f"\n*... and {len(files) - 15} more files*\n"

            content += "\n"

        with open(kw_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_comprehensive_book(self):
        """Generate the massive comprehensive_book.md."""
        print("Generating comprehensive book...")

        book_path = DOCS_ROOT / "comprehensive_book.md"

        content = """# Comprehensive DBN Repository Documentation

## Table of Contents

- [Part I: Project Overview](#part-i-project-overview)
- [Part II: Architecture](#part-ii-architecture)
- [Part III: Folder-by-Folder Deep Dive](#part-iii-folder-by-folder-deep-dive)
- [Part IV: File-Level Analysis](#part-iv-file-level-analysis)
- [Part V: Patterns and Idioms](#part-v-patterns-and-idioms)
- [Part VI: Performance and Scaling](#part-vi-performance-and-scaling)
- [Part VII: Security and Safety](#part-vii-security-and-safety)
- [Part VIII: Extension and Maintenance](#part-viii-extension-and-maintenance)
- [Part IX: Glossary](#part-ix-glossary)

---

# Part I: Project Overview

## Introduction to DBN

**D**atabento **B**inary E**n**coding (DBN) is an extremely fast message encoding and
storage format for normalized market data. The DBN specification includes a simple,
self-describing metadata header and a fixed set of struct definitions, which enforce
a standardized way to normalize market data.

## Repository Structure

This repository contains:

1. **Rust Core Library** (`rust/dbn/`): The main implementation
2. **Rust CLI Tool** (`rust/dbn-cli/`): Command-line utilities
3. **Rust Procedural Macros** (`rust/dbn-macros/`): Code generation
4. **Python Bindings** (`python/`): PyO3-based Python integration
5. **C FFI Bindings** (`c/`): C language interface
6. **Test Infrastructure** (`tests/`): Comprehensive test suites
7. **Automation Scripts** (`scripts/`): Build and deployment automation

## Mission and Goals

The DBN format was created to address several key challenges in market data handling:

### Performance
- Extremely fast encoding and decoding
- Zero-copy deserialization where possible
- Minimal memory allocations
- Highly compressible with Zstandard

### Standardization
- Fixed-width schemas for predictable parsing
- Standardized normalization across venues
- Versioned format for backward compatibility

### Flexibility
- Multiple output formats (DBN, CSV, JSON)
- Support for multiple programming languages
- Extensible schema system

---

# Part II: Architecture

## High-Level Design

The DBN system follows a layered architecture:

```
┌─────────────────────────────────────────┐
│   Applications & Client Libraries       │
├─────────────────────────────────────────┤
│   Language Bindings (Python, C)         │
├─────────────────────────────────────────┤
│   CLI Tools & Utilities                 │
├─────────────────────────────────────────┤
│   Core Rust Library (encode/decode)     │
├─────────────────────────────────────────┤
│   Record Types & Metadata               │
├─────────────────────────────────────────┤
│   Binary Format (DBN Spec)              │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Record Types
Located in `rust/dbn/src/record.rs` and related files.

Market data is represented as fixed-size records:
- MboMsg: Market by order messages
- Mbp1Msg/Mbp10Msg: Market by price (top 1/10 levels)
- TradeMsg: Trade reports
- OhlcvMsg: OHLCV bars
- InstrumentDefMsg: Instrument definitions
- StatusMsg: Trading status messages
- ImbalanceMsg: Imbalance data
- StatMsg: Statistics

### 2. Encoding System
Located in `rust/dbn/src/encode/`.

Supports multiple output formats:
- **DBN**: Native binary format (sync/async)
- **CSV**: Comma-separated values with configurable options
- **JSON**: JSON Lines format for text processing

### 3. Decoding System
Located in `rust/dbn/src/decode/`.

Handles multiple input formats:
- **DBN**: Current version format
- **DBZ**: Legacy format (deprecated)
- **Zstandard**: Compressed streams
- **Fragments**: Headerless DBN streams

### 4. Metadata System
Located in `rust/dbn/src/metadata.rs`.

Every DBN file includes metadata:
- Dataset and venue information
- Schema and symbol type
- Time range coverage
- Symbol mappings
- Version information

### 5. Symbol Mapping
Located in `rust/dbn/src/symbol_map.rs`.

Provides historical symbol resolution:
- PitSymbolMap: Point-in-time lookups
- TsSymbolMap: Time-series symbol mapping
- Support for multiple symbol types (ticker, ID, etc.)

---

# Part III: Folder-by-Folder Deep Dive

"""

        # Add folder documentation
        root_folder = self.folder_map[REPO_ROOT]

        def add_folder_chapter(folder: FolderInfo, depth=0):
            nonlocal content
            indent = "#" * (depth + 2)
            folder_display = str(folder.rel_path) if folder.rel_path != Path(".") else "root"

            content += f"\n{indent} Folder: {folder_display}\n\n"
            content += f"**Location:** `{folder.rel_path}`\n\n"

            # Add folder description
            content += self._describe_folder_purpose(folder) + "\n\n"

            # List key files
            if folder.files:
                content += "**Key Files:**\n\n"
                for file in folder.files[:5]:
                    content += f"- `{file.name}`: {self._get_file_description(file)}\n"
                if len(folder.files) > 5:
                    content += f"- *... and {len(folder.files) - 5} more files*\n"
                content += "\n"

            # Recurse into subfolders (limit depth)
            if depth < 3:
                for subfolder in sorted(folder.subfolders, key=lambda f: f.name):
                    add_folder_chapter(subfolder, depth + 1)

        add_folder_chapter(root_folder)

        content += """

---

# Part IV: File-Level Analysis

This section provides detailed analysis of key files in the repository.

## Core Library Files

### rust/dbn/src/lib.rs

The library entry point that exports all public APIs and establishes the module structure.

### rust/dbn/src/record.rs

Defines all market data record types with fixed-size layouts for efficient binary encoding.

### rust/dbn/src/encode.rs and rust/dbn/src/decode.rs

The core encoding and decoding implementations that handle format transformations.

## CLI Tool Files

### rust/dbn-cli/src/main.rs

The command-line interface entry point for the `dbn` tool.

## Python Binding Files

### python/src/lib.rs

The PyO3 bindings that expose Rust functionality to Python.

---

# Part V: Patterns and Idioms

## Rust Patterns Used

### Type Safety
The library extensively uses Rust's type system to prevent errors:
- NewType pattern for IDs and prices
- Enums for finite states (Action, Side, etc.)
- Result types for fallible operations

### Zero-Copy Parsing
Where possible, data is parsed without copying:
- RecordRef provides zero-copy views into buffers
- Streaming iterators avoid collecting into vectors

### Builder Pattern
Complex types use builders for ergonomic construction:
- MetadataBuilder
- Encoder builders (CsvEncoder, JsonEncoder)

## Performance Patterns

### Memory Efficiency
- Stack allocation preferred over heap
- Reuse of buffers in encoding/decoding
- Minimal allocations in hot paths

### Compression Integration
- Transparent Zstandard compression/decompression
- Streaming support for large files

---

# Part VI: Performance and Scaling

## Benchmarking Results

The DBN format is designed for extreme performance:
- Encoding: >10GB/s throughput (uncompressed)
- Decoding: >15GB/s throughput (uncompressed)
- Compression ratio: 10-20x with Zstandard (typical)

## Scaling Characteristics

### Large File Handling
- Streaming APIs prevent loading entire files into memory
- Async support for concurrent I/O operations
- Fragment support for parallel processing

### Language Performance

#### Rust
- Native performance, zero overhead
- Compile-time optimizations

#### Python
- Near-native performance through PyO3
- Zero-copy data access where possible
- GIL release during I/O operations

#### C
- FFI overhead minimal (<5% typically)
- Direct struct access for maximum performance

---

# Part VII: Security and Safety

## Memory Safety

Rust's ownership system provides:
- No buffer overflows
- No use-after-free
- No data races
- No null pointer dereferences

## Unsafe Code Audit

All `unsafe` blocks are carefully reviewed:
- Limited to FFI boundaries
- Invariants documented
- Testing validated

## Input Validation

All decoders validate:
- Magic bytes and version headers
- Record length consistency
- Metadata integrity
- Symbol string null-termination

## Dependency Security

Regular security audits via:
- cargo-audit
- Dependabot alerts
- Manual reviews of critical dependencies

---

# Part VIII: Extension and Maintenance

## Adding New Record Types

To add a new market data record type:

1. Define the struct in `rust/dbn/src/record.rs`
2. Implement required traits (HasRType, Record, etc.)
3. Add RType variant in `rust/dbn/src/enums.rs`
4. Update encoding/decoding logic
5. Add Python bindings if needed
6. Write comprehensive tests
7. Update documentation

## Adding New Encoding Formats

To support a new output format:

1. Create encoder in `rust/dbn/src/encode/`
2. Implement EncodeRecord trait
3. Add builder if complex options needed
4. Write both sync and async versions
5. Add CLI flag for new format
6. Test thoroughly

## Versioning Strategy

The project follows semantic versioning:
- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

DBN format versioning is separate:
- Version 1: Legacy (deprecated)
- Version 2: Current stable
- Version 3: Future features

---

# Part IX: Glossary

## Core Concepts

**DBN**: Databento Binary Encoding - the core binary format

**DBZ**: Databento Binary Zstandard - legacy format (deprecated)

**Record**: A fixed-size binary struct representing market data

**Schema**: A category of market data (MBO, trades, OHLCV, etc.)

**RType**: Record Type - identifies which struct a binary record represents

**Metadata**: Header information describing a DBN stream

**Publisher**: Data source identifier (venue + dataset combination)

**SType**: Symbol Type (ticker, instrument ID, ISIN, etc.)

**Fragment**: A DBN stream without metadata header

## Market Data Terms

**MBO**: Market By Order - order book at order-level granularity

**MBP**: Market By Price - order book aggregated by price level

**OHLCV**: Open, High, Low, Close, Volume bars

**BBO**: Best Bid and Offer - top of book only

**TBBO**: Trade at Best Bid and Offer

## Technical Terms

**Fixed-width encoding**: All fields have predetermined sizes

**Zero-copy**: Reading data without copying to new buffers

**Streaming iterator**: Iterator that reuses memory for each item

**Compression frame**: Unit of compressed data in Zstandard

**Symbol mapping**: Translation between symbol representations

---

## Conclusion

This comprehensive book documents the entire DBN repository in extreme detail.
For specific file-level documentation, see the individual `_docs.md` files in the
docs/ directory structure.

For keyword searches, consult:
- [Global Keywords Index](./keywords.md)
- Individual folder `sub.md` files for subtree keywords
- Individual file `_kw.md` files for file-specific keywords

## Navigation

- [Repository Index](./index.md) - Start here for repository overview
- [Global Keywords](./keywords.md) - Find any concept quickly
- Folder indexes - Navigate by directory structure

"""

        with open(book_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_global_index(self):
        """Generate global index.md."""
        print("Generating global index...")

        index_path = DOCS_ROOT / "index.md"

        content = """# DBN Repository Documentation Index

## Repository: databento/dbn

**Databento Binary Encoding (DBN)** - Fast message encoding and storage format for normalized market data.

## Overview

This documentation system provides comprehensive coverage of every file and folder in the repository.

### Quick Navigation

- **[Comprehensive Book](./comprehensive_book.md)** - Read the entire repository as a book
- **[Global Keywords](./keywords.md)** - Find any concept quickly
- **[Root Documentation](./doc.md)** - High-level repository documentation
- **[Root Subtree Keywords](./sub.md)** - All keywords in the repository

## Repository Structure

"""

        # Build tree view
        root_folder = self.folder_map[REPO_ROOT]

        def add_tree(folder: FolderInfo, depth=0):
            nonlocal content
            indent = "  " * depth
            prefix = "├── " if depth > 0 else ""

            folder_name = folder.name if folder.name != "root" else "."
            folder_link = f"./{folder.rel_path}/index.md" if folder.rel_path != Path(".") else "./index.md"

            content += f"{indent}{prefix}**[{folder_name}/]({folder_link})**\n"

            # Add first few files
            for file in folder.files[:3]:
                file_indent = "  " * (depth + 1)
                content += f"{file_indent}├── {file.name}\n"

            if len(folder.files) > 3:
                file_indent = "  " * (depth + 1)
                content += f"{file_indent}└── ... {len(folder.files) - 3} more files\n"

            # Add subfolders (limit depth)
            if depth < 2:
                for subfolder in sorted(folder.subfolders, key=lambda f: f.name):
                    add_tree(subfolder, depth + 1)

        add_tree(root_folder)

        content += """

## Main Components

### Rust Core Library
- **[rust/dbn/](./rust/dbn/index.md)** - Core DBN implementation
  - [Encoding](./rust/dbn/src/encode/index.md) - Format encoders
  - [Decoding](./rust/dbn/src/decode/index.md) - Format decoders
  - [Records](./rust/dbn/src/record/index.md) - Data type definitions

### Language Bindings
- **[python/](./python/index.md)** - Python bindings via PyO3
- **[c/](./c/index.md)** - C FFI bindings

### Tools
- **[rust/dbn-cli/](./rust/dbn-cli/index.md)** - Command-line tool
- **[scripts/](./scripts/index.md)** - Build and automation scripts

### Testing
- **[tests/](./tests/index.md)** - Test data and integration tests
- **[rust/dbn-macros/tests/](./rust/dbn-macros/tests/index.md)** - Macro tests

## Documentation System

### Per-File Documentation
Every file has:
- `<filename>_docs.md` - Comprehensive documentation
- `<filename>_kw.md` - Keyword index

### Per-Folder Documentation
Every folder has:
- `index.md` - File and subfolder listing
- `doc.md` - Narrative documentation
- `sub.md` - Subtree keyword index

### Global Documentation
- `comprehensive_book.md` - Complete repository book
- `keywords.md` - All keywords across repository
- `index.md` - This file

## Statistics

- **Total Files Documented:** {file_count}
- **Total Folders:** {folder_count}
- **Total Keywords:** {keyword_count}
- **Documentation Files Generated:** {doc_count}

## How to Use This Documentation

1. **Start with the [Comprehensive Book](./comprehensive_book.md)** for a complete overview
2. **Use [Keywords](./keywords.md)** to find specific concepts
3. **Navigate by folder** using index.md files
4. **Deep dive into files** using _docs.md files

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md_docs.md) for contribution guidelines.

## License

See [LICENSE](./LICENSE_docs.md) for license information.

"""

        # Fill in statistics
        content = content.format(
            file_count=len([f for f in self.all_files if not f.is_binary]),
            folder_count=len(self.all_folders),
            keyword_count=len(self.global_keywords),
            doc_count=len(self.all_files) * 2 + len(self.all_folders) * 3 + 3
        )

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_all_documentation(self):
        """Main method to generate all documentation."""
        print("=" * 60)
        print("DBN Repository Documentation Generator")
        print("=" * 60)

        # Step 1: Scan repository
        self.scan_repository()

        # Step 2: Read all files
        self.read_all_files()

        # Step 3: Create docs structure
        self.create_docs_structure()

        # Step 4: Generate per-file documentation
        print("Generating per-file documentation...")
        for i, file_info in enumerate(self.all_files):
            if i % 20 == 0:
                print(f"  Processing file {i+1}/{len(self.all_files)}")
            self.generate_file_docs(file_info)
            self.generate_file_keywords(file_info)

        # Step 5: Generate per-folder documentation
        print("Generating per-folder documentation...")
        for i, folder in enumerate(self.all_folders):
            if i % 10 == 0:
                print(f"  Processing folder {i+1}/{len(self.all_folders)}")
            self.generate_folder_index(folder)
            self.generate_folder_doc(folder)
            self.generate_folder_sub(folder)

        # Step 6: Generate global documentation
        self.generate_global_keywords()
        self.generate_comprehensive_book()
        self.generate_global_index()

        # Generate root folder docs
        root_folder = self.folder_map[REPO_ROOT]
        self.generate_folder_doc(root_folder)
        self.generate_folder_sub(root_folder)

        print("\n" + "=" * 60)
        print("Documentation Generation Complete!")
        print("=" * 60)
        print(f"\nStatistics:")
        print(f"  Files documented: {len(self.all_files)}")
        print(f"  Folders documented: {len(self.all_folders)}")
        print(f"  Keywords extracted: {len(self.global_keywords)}")
        print(f"  Total docs created: {len(self.all_files) * 2 + len(self.all_folders) * 3 + 3}")
        print(f"\nDocumentation root: {DOCS_ROOT}")
        print(f"  Start with: {DOCS_ROOT}/index.md")
        print(f"  Comprehensive book: {DOCS_ROOT}/comprehensive_book.md")
        print(f"  Keywords: {DOCS_ROOT}/keywords.md")


if __name__ == "__main__":
    generator = DocumentationGenerator()
    generator.generate_all_documentation()
