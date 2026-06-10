# PDF to Markdown Converter (Windows)

Converts PDF files to Markdown automatically by watching a folder.

## Requirements

- [Python 3](https://www.python.org/downloads/) — during installation, check **"Add Python to PATH"**
- [OpenJDK (Java)](https://adoptium.net/) — required by the PDF library

## How to use

1. **First time only:** double-click `start.bat` — it installs everything and offers to create desktop shortcuts
2. **Every time after:** double-click `start.bat` and minimise the window
3. **To convert:** drop any PDF into the **PDF Input** folder on your Desktop
4. The converted Markdown file appears in the **PDF Output** folder

Processed PDFs are moved to `input/done/` automatically.
