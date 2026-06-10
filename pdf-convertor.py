import argparse
import socket
import subprocess
import time
from pathlib import Path
from typing import Optional

import opendataloader_pdf

HYBRID_PORT = 5002


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def _start_hybrid_server() -> Optional[subprocess.Popen]:
    if _port_open(HYBRID_PORT):
        print(f"Hybrid server already running on port {HYBRID_PORT}.")
        return None
    print("Starting hybrid server...")
    cmd = ["opendataloader-pdf-hybrid", "--port", str(HYBRID_PORT)]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(1)
        if _port_open(HYBRID_PORT):
            print("Hybrid server ready.")
            return proc
    proc.terminate()
    raise RuntimeError("Hybrid server did not start within 30 seconds.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to Markdown in the outputs folder."
    )
    parser.add_argument("pdf_files", nargs="+", help="Path(s) to input PDF file(s); globs are accepted")
    parser.add_argument(
        "--no-hybrid",
        action="store_true",
        help="Disable hybrid mode (on by default)",
    )
    parser.add_argument(
        "--force-ocr",
        action="store_true",
        help="Force OCR on all pages (useful for scanned/image-based PDFs)",
    )
    parser.add_argument(
        "--image-output",
        choices=["external", "embedded", "off"],
        default="external",
        help="How to handle extracted images (default: external)",
    )
    args = parser.parse_args()

    pdf_paths = []
    for pattern in args.pdf_files:
        matches = list(Path().glob(pattern)) if "*" in pattern or "?" in pattern else [Path(pattern)]
        for p in matches:
            if not p.is_file():
                raise FileNotFoundError(f"Input file does not exist: {p}")
            if p.suffix.lower() != ".pdf":
                raise ValueError(f"Input file must be a .pdf: {p}")
            pdf_paths.append(p)

    if not pdf_paths:
        raise FileNotFoundError("No PDF files matched the given pattern(s).")

    server_proc = None
    if not args.no_hybrid:
        server_proc = _start_hybrid_server()

    groups: dict[Path, list[Path]] = {}
    for p in pdf_paths:
        groups.setdefault(p.parent, []).append(p)

    try:
        for parent, files in groups.items():
            output_dir = Path("outputs") / parent
            output_dir.mkdir(parents=True, exist_ok=True)

            convert_kwargs: dict = {
                "input_path": [str(p) for p in files],
                "output_dir": str(output_dir),
                "format": "markdown",
                "image_output": args.image_output,
            }
            if not args.no_hybrid:
                convert_kwargs["hybrid"] = "docling"
                convert_kwargs["use_struct_tree"] = True
                if args.force_ocr:
                    convert_kwargs["hybrid_ocr"] = "force"

            try:
                opendataloader_pdf.convert(**convert_kwargs)
            except subprocess.CalledProcessError as exc:
                if "StackOverflowError" not in (exc.output or "") or args.no_hybrid:
                    raise
                print("Hybrid mode crashed (StackOverflowError in reading-order algorithm). Retrying without hybrid...")
                convert_kwargs.pop("hybrid", None)
                convert_kwargs.pop("use_struct_tree", None)
                opendataloader_pdf.convert(**convert_kwargs)

            for pdf_path in files:
                md_path = output_dir / (pdf_path.stem + ".md")
                print(f"Done: {md_path}. To generate an index run:\n  /index-file {md_path}")
    finally:
        if server_proc is not None:
            server_proc.terminate()
            print("Hybrid server stopped.")


if __name__ == "__main__":
    main()
