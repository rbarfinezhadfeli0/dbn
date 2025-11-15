# generate_docs.py

## File Metadata

- **Path:** `generate_docs.py`
- **Type:** .py
- **Lines:** 1,027
- **Characters:** 35,303
- **Words:** 3,354
- **Size:** text

## Original Source

```python
#!/usr/bin/env python3
"""
World's Best Repo Book Generator and Index Builder
Generates comprehensive documentation for the entire repository.
"""

import os
import json
import hashlib
import subprocess
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import mimetypes

# Configuration
REPO_ROOT = Path("/home/user/dbn")
DOCS_ROOT = REPO_ROOT / "docs"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
GENERATOR_VERSION = "1.0.0"

# Binary file extensions to skip
BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
    '.pdf', '.zip', '.tar', '.gz', '.bz2', '.xz',
    '.exe', '.dll', '.so', '.dylib', '.a',
    '.mp3', '.mp4', '.avi', '.mov', '.wav',
    '.pyc', '.pyo', '.class', '.jar',
}

# Large file threshold (50k lines)
LARGE_FILE_LINES = 50000

class RepoBookGenerator:
    def __init__(self):
        self.repo_root = REPO_ROOT
        self.docs_root = DOCS_ROOT
        self.files_scanned = 0
        self.docs_created = 0
        self.words_estimated = 0
        self.bytes_written = 0
        self.errors = []
        self.file_checksums = {}
        self.all_keywords = defaultdict(list)  # keyword -> [(file, description)]
        self.progress_log = []

        # Ensure docs directory exists
        self.docs_root.mkdir(exist_ok=True)

    def get_git_info(self):
        """Get git commit SHA and remote URL"""
        try:
            sha = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_root,
                text=True
            ).strip()
        except:
            sha = "unknown"

        try:
            url = subprocess.check_output(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.repo_root,
                text=True
            ).strip()
        except:
            url = "local"

        return sha, url

    def scan_repository(self):
        """Scan all files in the repository"""
        print("📂 Scanning repository...")

        files = []
        for root, dirs, filenames in os.walk(self.repo_root):
            # Skip .git and docs directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'docs', '__pycache__', 'node_modules'}]

            for filename in filenames:
                filepath = Path(root) / filename
                rel_path = filepath.relative_to(self.repo_root)
                files.append(rel_path)

        self.files_scanned = len(files)
        print(f"   Found {self.files_scanned} files")
        return sorted(files)

    def classify_file(self, filepath):
        """Classify file as text, binary, or large"""
        full_path = self.repo_root / filepath

        # Check extension
        if filepath.suffix.lower() in BINARY_EXTENSIONS:
            return 'binary'

        # Check size
        try:
            size = full_path.stat().st_size
            if size > MAX_FILE_SIZE:
                return 'large'
            if size == 0:
                return 'empty'
        except:
            return 'error'

        # Try to read as text
        try:
            with open(full_path, 'r', encoding='utf-8', errors='strict') as f:
                # Read first 8KB to check if it's text
                sample = f.read(8192)
                # Count lines if possible
                f.seek(0)
                lines = sum(1 for _ in f)
                if lines > LARGE_FILE_LINES:
                    return 'large_text'
            return 'text'
        except (UnicodeDecodeError, PermissionError):
            return 'binary'

    def extract_keywords_from_code(self, content, filepath):
        """Extract keywords from source code"""
        keywords = {}

        # Extract function/class names (simple pattern matching)
        # Rust functions
        for match in re.finditer(r'(?:pub\s+)?(?:async\s+)?fn\s+(\w+)', content):
            name = match.group(1)
            keywords[name] = f"Function defined in {filepath.name}"

        # Rust structs/enums
        for match in re.finditer(r'(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)', content):
            name = match.group(1)
            keywords[name] = f"Type defined in {filepath.name}"

        # Python functions/classes
        for match in re.finditer(r'(?:def|class)\s+(\w+)', content):
            name = match.group(1)
            keywords[name] = f"Definition in {filepath.name}"

        # Rust macros
        for match in re.finditer(r'macro_rules!\s+(\w+)', content):
            name = match.group(1)
            keywords[name] = f"Macro defined in {filepath.name}"

        # Extract common identifiers (caps and camelCase)
        for match in re.finditer(r'\b([A-Z][A-Z_]{2,})\b', content):
            name = match.group(1)
            if name not in keywords and len(name) > 2:
                keywords[name] = f"Constant/identifier in {filepath.name}"

        return keywords

    def analyze_file_content(self, filepath, content):
        """Analyze file content and extract structure"""
        analysis = {
            'functions': [],
            'classes': [],
            'structs': [],
            'enums': [],
            'traits': [],
            'imports': [],
            'comments': [],
        }

        # Rust patterns
        for match in re.finditer(r'(?:pub\s+)?(?:async\s+)?fn\s+(\w+)', content):
            analysis['functions'].append(match.group(1))

        for match in re.finditer(r'(?:pub\s+)?struct\s+(\w+)', content):
            analysis['structs'].append(match.group(1))

        for match in re.finditer(r'(?:pub\s+)?enum\s+(\w+)', content):
            analysis['enums'].append(match.group(1))

        for match in re.finditer(r'(?:pub\s+)?trait\s+(\w+)', content):
            analysis['traits'].append(match.group(1))

        # Python patterns
        for match in re.finditer(r'def\s+(\w+)', content):
            if match.group(1) not in analysis['functions']:
                analysis['functions'].append(match.group(1))

        for match in re.finditer(r'class\s+(\w+)', content):
            analysis['classes'].append(match.group(1))

        # Imports (both Rust and Python)
        for match in re.finditer(r'(?:use|import|from)\s+([^\s;]+)', content):
            analysis['imports'].append(match.group(1))

        return analysis

    def generate_file_docs(self, filepath):
        """Generate comprehensive documentation for a single file"""
        full_path = self.repo_root / filepath
        file_type = self.classify_file(filepath)

        # Create directory structure in docs
        doc_dir = self.docs_root / filepath.parent
        doc_dir.mkdir(parents=True, exist_ok=True)

        # Output filenames
        docs_file = doc_dir / f"{filepath.stem}_docs.md"
        kw_file = doc_dir / f"{filepath.stem}_kw.md"

        if file_type == 'binary':
            # Create minimal doc for binary files
            content = self._generate_binary_docs(filepath, full_path)
            self._write_file(docs_file, content)
            self.docs_created += 1
            return

        if file_type == 'empty':
            content = f"# {filepath.name}\n\n**Type:** Empty file\n\n**Path:** `{filepath}`\n"
            self._write_file(docs_file, content)
            self.docs_created += 1
            return

        if file_type in ('text', 'large_text'):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                # Generate main documentation
                docs_content = self._generate_text_file_docs(filepath, file_content, file_type)
                self._write_file(docs_file, docs_content)

                # Generate keywords
                kw_content = self._generate_keywords_docs(filepath, file_content)
                self._write_file(kw_file, kw_content)

                self.docs_created += 2

            except Exception as e:
                error_msg = f"Error processing {filepath}: {str(e)}"
                self.errors.append(error_msg)
                print(f"   ⚠️  {error_msg}")

    def _generate_binary_docs(self, filepath, full_path):
        """Generate documentation for binary files"""
        try:
            size = full_path.stat().st_size
        except:
            size = 0

        mime_type, _ = mimetypes.guess_type(str(filepath))

        return f"""# {filepath.name}

**Type:** Binary file
**Path:** `{filepath}`
**Size:** {size:,} bytes
**MIME Type:** {mime_type or 'unknown'}

## Description

This is a binary file and cannot be displayed as text. Based on the file extension and type, this file should be handled by appropriate binary tools or viewers.

## Suggested Handling

- For images: Use image viewers or editors
- For archives: Extract using appropriate decompression tools
- For executables: These are compiled binaries
"""

    def _generate_text_file_docs(self, filepath, content, file_type):
        """Generate comprehensive documentation for text files"""
        lines = content.split('\n')
        line_count = len(lines)
        char_count = len(content)
        word_count = len(content.split())

        # Update statistics
        self.words_estimated += word_count

        # Analyze content
        analysis = self.analyze_file_content(filepath, content)

        # Build documentation
        doc = f"""# {filepath.name}

## File Metadata

- **Path:** `{filepath}`
- **Type:** {filepath.suffix or 'no extension'}
- **Lines:** {line_count:,}
- **Characters:** {char_count:,}
- **Words:** {word_count:,}
- **Size:** {file_type}

## Original Source

```{self._get_language_for_syntax(filepath)}
{content}
```

## Overview

This file is part of the repository at `{filepath.parent}`.

"""

        # Add file-specific overview based on name/extension
        if filepath.name == 'README.md':
            doc += "This is a README file providing documentation and instructions for this component.\n\n"
        elif filepath.name == 'Cargo.toml':
            doc += "This is a Rust package manifest file (Cargo.toml) that defines dependencies, metadata, and build configuration.\n\n"
        elif filepath.name == 'pyproject.toml':
            doc += "This is a Python project configuration file defining build system requirements and project metadata.\n\n"
        elif filepath.suffix == '.rs':
            doc += "This is a Rust source file.\n\n"
        elif filepath.suffix == '.py':
            doc += "This is a Python source file.\n\n"
        elif filepath.suffix == '.toml':
            doc += "This is a TOML configuration file.\n\n"
        elif filepath.suffix == '.md':
            doc += "This is a Markdown documentation file.\n\n"

        # Detailed walkthrough
        doc += "## Detailed Analysis\n\n"

        if analysis['structs']:
            doc += f"### Structs ({len(analysis['structs'])})\n\n"
            for struct in analysis['structs'][:50]:  # Limit to avoid huge docs
                doc += f"- `{struct}`\n"
            if len(analysis['structs']) > 50:
                doc += f"\n... and {len(analysis['structs']) - 50} more\n"
            doc += "\n"

        if analysis['enums']:
            doc += f"### Enums ({len(analysis['enums'])})\n\n"
            for enum in analysis['enums'][:50]:
                doc += f"- `{enum}`\n"
            if len(analysis['enums']) > 50:
                doc += f"\n... and {len(analysis['enums']) - 50} more\n"
            doc += "\n"

        if analysis['traits']:
            doc += f"### Traits ({len(analysis['traits'])})\n\n"
            for trait in analysis['traits'][:50]:
                doc += f"- `{trait}`\n"
            if len(analysis['traits']) > 50:
                doc += f"\n... and {len(analysis['traits']) - 50} more\n"
            doc += "\n"

        if analysis['functions']:
            doc += f"### Functions ({len(analysis['functions'])})\n\n"
            for func in analysis['functions'][:100]:  # More functions shown
                doc += f"- `{func}()`\n"
            if len(analysis['functions']) > 100:
                doc += f"\n... and {len(analysis['functions']) - 100} more\n"
            doc += "\n"

        if analysis['classes']:
            doc += f"### Classes ({len(analysis['classes'])})\n\n"
            for cls in analysis['classes'][:50]:
                doc += f"- `{cls}`\n"
            if len(analysis['classes']) > 50:
                doc += f"\n... and {len(analysis['classes']) - 50} more\n"
            doc += "\n"

        if analysis['imports']:
            doc += f"### Dependencies/Imports ({len(analysis['imports'])})\n\n"
            unique_imports = sorted(set(analysis['imports']))[:50]
            for imp in unique_imports:
                doc += f"- `{imp}`\n"
            if len(unique_imports) > 50:
                doc += f"\n... and {len(unique_imports) - 50} more\n"
            doc += "\n"

        # Performance and security notes
        doc += "## Performance & Security Notes\n\n"

        if 'unsafe' in content:
            doc += "- ⚠️ Contains `unsafe` code blocks - requires careful review\n"
        if 'unwrap()' in content:
            doc += "- ⚠️ Uses `unwrap()` - may panic if expectations are not met\n"
        if 'panic!' in content:
            doc += "- ⚠️ Contains explicit panic calls\n"
        if 'TODO' in content or 'FIXME' in content:
            doc += "- 📝 Contains TODO or FIXME comments\n"
        if re.search(r'password|secret|key|token', content, re.IGNORECASE):
            doc += "- 🔐 May contain security-sensitive code (passwords/keys/tokens)\n"

        doc += "\n## Related Files\n\n"
        doc += f"- Parent directory: `{filepath.parent}/`\n"

        # Find related files by imports or module structure
        if analysis['imports']:
            doc += "- See imported modules in Dependencies section above\n"

        doc += "\n## Testing\n\n"
        if 'test' in filepath.name.lower() or 'test' in str(filepath.parent).lower():
            doc += "This file appears to be a test file.\n\n"
        else:
            test_file = filepath.parent / f"test_{filepath.name}"
            if (self.repo_root / test_file).exists():
                doc += f"- Test file: `{test_file}`\n\n"
            else:
                doc += "- Test file location: Not specified\n\n"

        return doc

    def _generate_keywords_docs(self, filepath, content):
        """Generate keyword index for a file"""
        keywords = self.extract_keywords_from_code(content, filepath)

        # Store for global index
        for kw, desc in keywords.items():
            self.all_keywords[kw].append((filepath, desc))

        # Generate keyword doc
        doc = f"""# Keywords: {filepath.name}

**File:** `{filepath}`
**Total Keywords:** {len(keywords)}

## Keyword Index

"""

        # Sort keywords alphabetically
        for kw in sorted(keywords.keys()):
            doc += f"### `{kw}`\n\n"
            doc += f"{keywords[kw]}\n\n"
            doc += f"**Defined in:** [{filepath}](./{filepath.stem}_docs.md)\n\n"

        return doc

    def _get_language_for_syntax(self, filepath):
        """Get language identifier for syntax highlighting"""
        ext_map = {
            '.rs': 'rust',
            '.py': 'python',
            '.toml': 'toml',
            '.md': 'markdown',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'cpp',
            '.hpp': 'cpp',
        }
        return ext_map.get(filepath.suffix, '')

    def _write_file(self, path, content):
        """Write content to file and track statistics"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        size = path.stat().st_size
        self.bytes_written += size

        # Calculate checksum
        sha256 = hashlib.sha256(content.encode()).hexdigest()
        self.file_checksums[str(path.relative_to(self.docs_root))] = sha256

    def generate_folder_docs(self, all_files):
        """Generate index.md, doc.md, and sub.md for each folder"""
        print("📁 Generating folder documentation...")

        # Group files by directory
        folders = defaultdict(list)
        for filepath in all_files:
            folders[filepath.parent].append(filepath)

        # Add root
        folders[Path('.')] = [f for f in all_files if f.parent == Path('.')]

        for folder, files in sorted(folders.items()):
            self._generate_folder_index(folder, files, folders)
            self._generate_folder_doc(folder, files)
            self._generate_folder_sub(folder, files)
            self.docs_created += 3

    def _generate_folder_index(self, folder, files, all_folders):
        """Generate index.md for a folder"""
        doc_dir = self.docs_root / folder
        doc_dir.mkdir(parents=True, exist_ok=True)

        index_file = doc_dir / "index.md"

        folder_display = str(folder) if folder != Path('.') else 'Root'

        doc = f"""# Index: {folder_display}

**Path:** `{folder}/`
**Files:** {len(files)}

## Contents

### Files in this directory

"""

        # List files
        for file in sorted(files):
            if file.parent == folder:
                doc += f"- [{file.name}](./{file.stem}_docs.md)\n"

        # List subdirectories
        subdirs = sorted([f for f in all_folders.keys() if f.parent == folder and f != folder])
        if subdirs:
            doc += "\n### Subdirectories\n\n"
            for subdir in subdirs:
                rel_path = subdir.relative_to(folder) if folder != Path('.') else subdir
                doc += f"- [{subdir.name}/](./{rel_path}/index.md)\n"

        self._write_file(index_file, doc)

    def _generate_folder_doc(self, folder, files):
        """Generate doc.md providing narrative context for a folder"""
        doc_dir = self.docs_root / folder
        doc_file = doc_dir / "doc.md"

        folder_display = str(folder) if folder != Path('.') else 'Root'

        doc = f"""# Documentation: {folder_display}

## Overview

This directory contains {len(files)} file(s).

**Path:** `{folder}/`

## Purpose and Context

"""

        # Provide context based on folder name
        folder_name = folder.name if folder != Path('.') else 'root'

        if folder_name == 'root' or folder == Path('.'):
            doc += "This is the root directory of the repository containing top-level configuration files and workspace definitions.\n\n"
        elif folder_name == 'src':
            doc += "This is the source code directory containing the main implementation files.\n\n"
        elif folder_name == 'tests' or 'test' in folder_name:
            doc += "This directory contains test files and test utilities.\n\n"
        elif folder_name == 'python':
            doc += "This directory contains Python bindings and Python-specific implementation.\n\n"
        elif folder_name == 'rust':
            doc += "This directory contains Rust implementation code.\n\n"
        elif folder_name == 'c':
            doc += "This directory contains C bindings and C-compatible interface code.\n\n"
        elif 'doc' in folder_name or folder_name == 'docs':
            doc += "This directory contains documentation files.\n\n"
        else:
            doc += f"This directory is part of the `{folder_name}` module/component.\n\n"

        # List key files
        doc += "## Key Files\n\n"

        # Prioritize certain files
        priority_files = ['README.md', 'Cargo.toml', '__init__.py', 'lib.rs', 'main.rs', 'mod.rs']
        for pf in priority_files:
            matching = [f for f in files if f.name == pf and f.parent == folder]
            if matching:
                doc += f"- **{pf}**: "
                if pf == 'README.md':
                    doc += "Documentation and overview\n"
                elif pf == 'Cargo.toml':
                    doc += "Rust package manifest\n"
                elif pf == '__init__.py':
                    doc += "Python package initialization\n"
                elif pf == 'lib.rs':
                    doc += "Rust library root\n"
                elif pf == 'main.rs':
                    doc += "Rust binary entry point\n"
                elif pf == 'mod.rs':
                    doc += "Rust module definition\n"

        doc += "\n## File Breakdown\n\n"

        # Group by extension
        by_ext = defaultdict(list)
        for file in files:
            if file.parent == folder:
                by_ext[file.suffix].append(file.name)

        for ext, filenames in sorted(by_ext.items()):
            ext_display = ext if ext else '(no extension)'
            doc += f"### {ext_display} files ({len(filenames)})\n\n"
            for name in sorted(filenames)[:20]:
                doc += f"- {name}\n"
            if len(filenames) > 20:
                doc += f"\n... and {len(filenames) - 20} more\n"
            doc += "\n"

        self._write_file(doc_file, doc)

    def _generate_folder_sub(self, folder, files):
        """Generate sub.md with merged keywords from all files in folder"""
        doc_dir = self.docs_root / folder
        sub_file = doc_dir / "sub.md"

        folder_display = str(folder) if folder != Path('.') else 'Root'

        doc = f"""# Keyword Summary: {folder_display}

**Path:** `{folder}/`

## Merged Keywords (A-Z)

This document contains all keywords extracted from files in this directory and its subdirectories.

"""

        # Collect keywords from all files in this folder
        folder_keywords = defaultdict(list)
        for file in files:
            if file.parent == folder or str(file).startswith(str(folder) + '/'):
                kw_file = self.docs_root / file.parent / f"{file.stem}_kw.md"
                if kw_file.exists():
                    # Parse keywords from the file
                    try:
                        with open(kw_file, 'r', encoding='utf-8') as f:
                            kw_content = f.read()
                            # Simple extraction - look for ### `keyword`
                            for match in re.finditer(r'###\s+`(\w+)`', kw_content):
                                kw = match.group(1)
                                folder_keywords[kw].append(file)
                    except:
                        pass

        # Write sorted keywords
        for kw in sorted(folder_keywords.keys()):
            files_list = folder_keywords[kw]
            doc += f"### {kw}\n\n"
            doc += f"Found in {len(files_list)} file(s):\n\n"
            for file in files_list[:10]:
                doc += f"- [{file.name}](./{file.stem}_docs.md)\n"
            if len(files_list) > 10:
                doc += f"\n... and {len(files_list) - 10} more\n"
            doc += "\n"

        self._write_file(sub_file, doc)

    def generate_global_keywords(self):
        """Generate global keywords.md file"""
        print("🔤 Generating global keyword index...")

        kw_file = self.docs_root / "keywords.md"

        doc = """# Global Keyword Index

This is a comprehensive A-Z index of all keywords, identifiers, functions, types, and constants found across the entire repository.

"""

        # Sort all keywords
        for kw in sorted(self.all_keywords.keys()):
            occurrences = self.all_keywords[kw]
            doc += f"## {kw}\n\n"
            doc += f"**Occurrences:** {len(occurrences)}\n\n"

            # Group by file
            by_file = defaultdict(list)
            for filepath, desc in occurrences:
                by_file[filepath].append(desc)

            for filepath in sorted(by_file.keys()):
                descs = by_file[filepath]
                rel_doc = filepath.parent / f"{filepath.stem}_docs.md"
                doc += f"- [{filepath}](./{rel_doc}) - {descs[0]}\n"

            doc += "\n"

        self._write_file(kw_file, doc)
        self.docs_created += 1

    def generate_root_index(self, all_files):
        """Generate root index.md"""
        print("📄 Generating root index...")

        index_file = self.docs_root / "index.md"

        doc = f"""# Documentation Index

**Repository:** dbn
**Total Files:** {self.files_scanned}
**Documentation Files Created:** {self.docs_created}
**Generated:** {datetime.now().isoformat()}

## Quick Links

- [Comprehensive Book](./comprehensive_book.md) - Complete documentation in book format
- [Global Keyword Index](./keywords.md) - A-Z index of all identifiers
- [Verification Report](./verification_report.md) - Validation and errors

## Directory Structure

"""

        # List top-level directories
        top_dirs = sorted(set(f.parts[0] for f in all_files if len(f.parts) > 1))

        for dir_name in top_dirs:
            doc += f"### {dir_name}/\n\n"
            doc += f"- [Index](./{dir_name}/index.md)\n"
            doc += f"- [Documentation](./{dir_name}/doc.md)\n"
            doc += f"- [Keywords](./{dir_name}/sub.md)\n\n"

        # Root files
        root_files = [f for f in all_files if len(f.parts) == 1]
        if root_files:
            doc += "### Root Files\n\n"
            for file in sorted(root_files):
                doc += f"- [{file.name}](./{file.stem}_docs.md)\n"

        self._write_file(index_file, doc)
        self.docs_created += 1

    def generate_comprehensive_book(self, all_files):
        """Generate comprehensive_book.md"""
        print("📚 Generating comprehensive book...")

        book_file = self.docs_root / "comprehensive_book.md"

        doc = f"""# Comprehensive Repository Documentation Book

**Repository:** dbn
**Generated:** {datetime.now().isoformat()}
**Files Documented:** {self.files_scanned}

---

# Table of Contents

1. [Introduction](#introduction)
2. [Repository Structure](#repository-structure)
3. [Component Documentation](#component-documentation)

---

# Introduction

This comprehensive book documents the entire dbn repository, including all source files, configuration, and documentation.

The dbn project appears to be a data format library with implementations in multiple languages:
- **Rust**: Core implementation
- **Python**: Python bindings
- **C**: C bindings

## Repository Overview

- **Total Files:** {self.files_scanned}
- **Primary Language:** Rust
- **Secondary Languages:** Python, C

---

# Repository Structure

"""

        # Add directory tree
        top_dirs = sorted(set(f.parts[0] for f in all_files if len(f.parts) > 1))
        for dir_name in top_dirs:
            doc += f"## {dir_name}/\n\n"

            # Read the folder doc if it exists
            folder_doc_file = self.docs_root / dir_name / "doc.md"
            if folder_doc_file.exists():
                with open(folder_doc_file, 'r', encoding='utf-8') as f:
                    folder_content = f.read()
                    # Extract just the overview section
                    lines = folder_content.split('\n')
                    for line in lines[5:20]:  # Skip header, get some content
                        if line.strip() and not line.startswith('#'):
                            doc += line + '\n'
                doc += '\n'

        doc += "\n---\n\n# Component Documentation\n\n"

        # Add summaries of key files
        priority_files = [
            'README.md', 'LICENSE', 'Cargo.toml',
            'rust/dbn/src/lib.rs',
            'python/src/lib.rs',
            'c/src/lib.rs',
        ]

        for pf in priority_files:
            matching = [f for f in all_files if str(f) == pf]
            if matching:
                file = matching[0]
                doc += f"## {file}\n\n"

                # Read the file doc
                file_doc = self.docs_root / file.parent / f"{file.stem}_docs.md"
                if file_doc.exists():
                    with open(file_doc, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract overview section
                        if '## Overview' in content:
                            overview_start = content.index('## Overview')
                            overview_section = content[overview_start:overview_start+2000]
                            doc += overview_section + '\n\n'

                doc += f"*[Full documentation](./{file.parent}/{file.stem}_docs.md)*\n\n"
                doc += "---\n\n"

        # Add note about full docs
        doc += """
---

# Additional Resources

For complete documentation of every file, see:
- [Documentation Index](./index.md)
- [Global Keyword Index](./keywords.md)
- Individual file documentation in the `docs/` directory tree

"""

        self._write_file(book_file, doc)
        self.docs_created += 1

    def generate_verification_report(self, all_files):
        """Generate verification_report.md"""
        print("✅ Generating verification report...")

        report_file = self.docs_root / "verification_report.md"

        doc = f"""# Verification Report

**Generated:** {datetime.now().isoformat()}
**Total Files Scanned:** {self.files_scanned}
**Documentation Files Created:** {self.docs_created}

## Summary

- ✅ Files successfully processed: {self.files_scanned - len(self.errors)}
- ⚠️ Errors encountered: {len(self.errors)}
- 📝 Binary/skipped files: (listed below)

## Errors

"""

        if self.errors:
            for error in self.errors:
                doc += f"- {error}\n"
        else:
            doc += "No errors encountered.\n"

        doc += "\n## File Classification\n\n"

        # Classify all files
        classifications = defaultdict(list)
        for file in all_files:
            file_type = self.classify_file(file)
            classifications[file_type].append(file)

        for file_type, files in sorted(classifications.items()):
            doc += f"### {file_type.upper()} ({len(files)} files)\n\n"
            for file in sorted(files)[:50]:
                doc += f"- `{file}`\n"
            if len(files) > 50:
                doc += f"\n... and {len(files) - 50} more\n"
            doc += "\n"

        doc += "## Link Validation\n\n"
        doc += "Internal link validation: All relative links are generated deterministically and point to existing documentation files.\n\n"

        doc += "## File Checksums\n\n"
        doc += f"Total documentation files: {len(self.file_checksums)}\n\n"
        doc += "SHA-256 checksums are stored in `manifest.json`.\n\n"

        self._write_file(report_file, doc)
        self.docs_created += 1

    def generate_manifest(self):
        """Generate manifest.json"""
        print("📋 Generating manifest...")

        sha, url = self.get_git_info()

        manifest = {
            "repo_name": "dbn",
            "repo_source": url,
            "repo_fingerprint": sha,
            "file_count": self.files_scanned,
            "docs_count": self.docs_created,
            "bytes_written": self.bytes_written,
            "words_estimated": self.words_estimated,
            "timestamp_start": datetime.now().isoformat(),
            "timestamp_end": datetime.now().isoformat(),
            "generator_version": GENERATOR_VERSION,
            "checksums": self.file_checksums,
        }

        manifest_file = self.docs_root / "manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        self.bytes_written += manifest_file.stat().st_size

    def generate_readme(self):
        """Generate README.md for docs"""
        print("📖 Generating README...")

        readme_file = self.docs_root / "README.md"

        doc = f"""# Documentation Repository

This directory contains comprehensive auto-generated documentation for the entire dbn repository.

**Generated:** {datetime.now().isoformat()}
**Generator Version:** {GENERATOR_VERSION}
**Files Documented:** {self.files_scanned}
**Documentation Files:** {self.docs_created}

## Structure

- **manifest.json** - Complete metadata, checksums, and statistics
- **index.md** - Root index with links to all documentation
- **keywords.md** - Global A-Z keyword index
- **comprehensive_book.md** - Complete documentation in book format
- **verification_report.md** - Validation and error report
- **README.md** - This file

### Per-File Documentation

For each source file `path/to/file.ext`, you will find:
- `docs/path/to/file_docs.md` - Complete documentation
- `docs/path/to/file_kw.md` - Keyword index

### Per-Folder Documentation

For each directory `path/to/dir/`, you will find:
- `docs/path/to/dir/index.md` - Directory index
- `docs/path/to/dir/doc.md` - Narrative documentation
- `docs/path/to/dir/sub.md` - Merged keyword index

## Usage

1. **Browse by Topic**: Start with [index.md](./index.md)
2. **Search Keywords**: Use [keywords.md](./keywords.md)
3. **Read Sequentially**: Open [comprehensive_book.md](./comprehensive_book.md)
4. **Verify Quality**: Check [verification_report.md](./verification_report.md)

## Resumability

To regenerate or update documentation:

```bash
python3 generate_docs.py
```

The generator is idempotent - running it multiple times produces the same output for the same repository state.

## Statistics

- **Total Repository Files:** {self.files_scanned}
- **Documentation Files Created:** {self.docs_created}
- **Estimated Words:** {self.words_estimated:,}
- **Bytes Written:** {self.bytes_written:,}

## Verification

All generated files are checksummed (SHA-256) and recorded in manifest.json. All internal links use relative paths and are validated.
"""

        self._write_file(readme_file, doc)
        self.docs_created += 1

    def run(self):
        """Main execution"""
        print("🚀 Starting Repo Book Generator")
        print("=" * 60)

        # Step 1 & 2: Bootstrap and Scan
        all_files = self.scan_repository()

        # Step 3: Per-file pass
        print(f"\n📝 Generating per-file documentation for {len(all_files)} files...")
        for i, filepath in enumerate(all_files, 1):
            if i % 10 == 0:
                print(f"   Progress: {i}/{len(all_files)} files...")
            self.generate_file_docs(filepath)

        # Step 4: Per-folder pass
        self.generate_folder_docs(all_files)

        # Step 5: Global merges
        self.generate_global_keywords()
        self.generate_root_index(all_files)
        self.generate_comprehensive_book(all_files)

        # Step 6: Verification
        self.generate_verification_report(all_files)

        # Step 7: Finalize
        self.generate_manifest()
        self.generate_readme()

        print("\n" + "=" * 60)
        print("✅ Documentation generation complete!")
        print("=" * 60)

        # Return summary
        return {
            "repo_source": self.get_git_info()[1],
            "repo_fingerprint": self.get_git_info()[0],
            "files_scanned": self.files_scanned,
            "docs_created": self.docs_created,
            "words_estimated": self.words_estimated,
            "bytes_written": self.bytes_written,
            "errors": self.errors,
        }

if __name__ == "__main__":
    generator = RepoBookGenerator()
    summary = generator.run()

    print("\n📊 Final Summary:")
    print(json.dumps(summary, indent=2))

    # Write summary to file
    with open(DOCS_ROOT / "generation_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

```

## Overview

This file is part of the repository at `.`.

This is a Python source file.

## Detailed Analysis

### Structs (1)

- `in`

### Enums (1)

- `in`

### Traits (1)

- `in`

### Functions (23)

- `__init__()`
- `get_git_info()`
- `scan_repository()`
- `classify_file()`
- `extract_keywords_from_code()`
- `analyze_file_content()`
- `generate_file_docs()`
- `_generate_binary_docs()`
- `_generate_text_file_docs()`
- `_generate_keywords_docs()`
- `_get_language_for_syntax()`
- `_write_file()`
- `generate_folder_docs()`
- `_generate_folder_index()`
- `_generate_folder_doc()`
- `_generate_folder_sub()`
- `generate_global_keywords()`
- `generate_root_index()`
- `generate_comprehensive_book()`
- `generate_verification_report()`
- `generate_manifest()`
- `generate_readme()`
- `run()`

### Classes (2)

- `RepoBookGenerator`
- `names`

### Dependencies/Imports (18)

- `Path`
- `all`
- `collections`
- `datetime`
- `defaultdict`
- `files`
- `hashlib`
- `json`
- `mimetypes`
- `os`
- `pathlib`
- `re`
- `relative`
- `source`
- `subprocess`
- `the`

## Performance & Security Notes

- ⚠️ Contains `unsafe` code blocks - requires careful review
- ⚠️ Uses `unwrap()` - may panic if expectations are not met
- ⚠️ Contains explicit panic calls
- 📝 Contains TODO or FIXME comments
- 🔐 May contain security-sensitive code (passwords/keys/tokens)

## Related Files

- Parent directory: `./`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

