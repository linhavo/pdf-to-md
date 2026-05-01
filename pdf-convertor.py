import argparse
from pathlib import Path

import opendataloader_pdf


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to Markdown in the outputs folder."
    )
    parser.add_argument("pdf_file", help="Path to the input PDF file")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a .pdf")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    opendataloader_pdf.convert(
        input_path=[str(pdf_path)],
        output_dir=str(output_dir),
        format="markdown",
    )


if __name__ == "__main__":
    main()


