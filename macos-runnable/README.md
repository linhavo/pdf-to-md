# PDF to Markdown Converter (macOS)

Converts PDF files to Markdown automatically by watching a folder.

## Requirements

- [Python 3](https://www.python.org/downloads/) — or via Homebrew: `brew install python`
- [OpenJDK (Java)](https://adoptium.net/) — required by the PDF library, or via Homebrew: `brew install openjdk`

## How to use

1. **First time only:** double-click `start.command` — it installs everything automatically
   - If macOS blocks it: right-click → Open → Open
2. **Every time after:** double-click `start.command` and keep the terminal window open
3. **To convert:** drop any PDF into the **input/** folder next to `start.command`
4. The converted Markdown file appears in the **output/** folder

Processed PDFs are moved to `input/done/` automatically.
