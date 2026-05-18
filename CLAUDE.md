# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**opendataloader-pdf-convertor** is a Python utility that converts PDF files to Markdown format using the `opendataloader-pdf` library. The converted markdown is stored in the `outputs/` directory, making it readable and processable for text analysis and AI tools like Claude.

### Key Use Case
When working with large PDF documents (especially technical/academic papers), convert them to Markdown to enable:
- Efficient scanning via TABLE OF CONTENTS or INDEX files
- Chunked reading when files exceed token limits
- Better text parsing and structured analysis

## Setup & Environment

### Initial Setup
```bash
# Run the setup script (installs JDK if needed, creates venv, installs dependencies)
./setup.sh

# Activate virtual environment
source .venv/bin/activate
```

**Requirements:**
- OpenJDK (Java Development Kit) — required by the PDF converter library
- Python 3.x
- Dependencies listed in `requirements.txt` (opendataloader-pdf==1.8.1)

### After Activation
Once `.venv` is activated, all subsequent Python commands use the isolated environment.

## Common Commands

### Convert a PDF to Markdown
```bash
python pdf-convertor.py <path/to/file.pdf>
```
- Takes PDF file path as argument
- Creates `outputs/` directory if it doesn't exist
- Outputs Markdown file named after the input PDF (e.g., `file.md`)
- Also generates an images folder (`<filename>_images/`) for extracted images

### Create an INDEX File for Large Markdown Documents
When a converted markdown file is very large (>20k tokens), create an index:
```bash
# Manually create <filename>_INDEX.md with:
# - Complete table of contents
# - Section descriptions
# - Quick reference guide
# - Key topics/research questions
```
This allows Claude to scan the index first before requesting specific sections from the full file.

## Project Structure

```
.
├── pdf-convertor.py          # Main conversion script
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script (JDK + venv + pip install)
├── .venv/                    # Python virtual environment
├── outputs/                  # Converted markdown files and images
│   ├── <filename>.md         # Converted markdown
│   ├── <filename>_INDEX.md   # Index for large files (if created)
│   └── <filename>_images/    # Extracted images
└── .gitignore               # Excludes .venv, __pycache__, outputs/, *.pdf
```

### Important Ignore Patterns
- `outputs/` and `*.pdf` are gitignored (they're large binaries and generated content)
- `.venv/` is gitignored (environment is environment-specific)

## Working with Large Documents

### When Converting a Large PDF

1. **First Conversion**: `python pdf-convertor.py document.pdf`
   - Produces `outputs/document.md` (might be very large)
   - Produces `outputs/document_images/` folder

2. **Create an INDEX** (if file is >25k tokens):
   - Read the markdown file structure
   - Create `outputs/document_INDEX.md` with table of contents, section descriptions, and quick reference
   - Include page/line numbers and topic keywords

3. **Using the INDEX with Claude**:
   - Claude scans the INDEX first (~2-5k tokens)
   - User specifies which section/chapter to read from the full file
   - More efficient than loading entire large file

### Example Pattern (Already Used)
- PDF: `DP_Verze pro OŠ_16.5..pdf` → Converted to `DP_Verze pro OŠ_16.5..md` (~85k tokens)
- INDEX: Created `DP_Verze pro OŠ_16.5._INDEX.md` with full chapter breakdown and quick reference
- Result: Claude can now efficiently work with this large document by scanning index first

## Architecture Notes

The converter is thin wrapper around `opendataloader-pdf`:
- **Input**: PDF file path (validated for existence and .pdf extension)
- **Processing**: Uses `opendataloader_pdf.convert()` with format="markdown"
- **Output**: Markdown + images to `outputs/` directory
- **Error Handling**: Raises FileNotFoundError or ValueError for invalid input

No complex logic in the converter itself — all PDF parsing and markdown generation is handled by the `opendataloader-pdf` library.

## Development Notes

- **Language**: Python 3
- **Dependencies**: Single production dependency (`opendataloader-pdf==1.8.1`)
- **No tests/linting**: This is a simple utility script, not a library
- **Local PDF files**: Stored in repo root during development (gitignored for final commits)

## When Creating New Conversations

- Always check for INDEX files in `outputs/` before working with converted markdown
- For large documents, suggest creating an INDEX if one doesn't exist
- Remember: converted markdown files go to `outputs/`, never modify source PDFs
