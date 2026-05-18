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
    proc = subprocess.Popen(
        ["opendataloader-pdf-hybrid", "--port", str(HYBRID_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
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
    parser.add_argument("pdf_file", help="Path to the input PDF file")
    parser.add_argument(
        "--no-hybrid",
        action="store_true",
        help="Disable hybrid mode (on by default)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a .pdf")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    server_proc = None
    if not args.no_hybrid:
        server_proc = _start_hybrid_server()

    try:
        opendataloader_pdf.convert(
            input_path=[str(pdf_path)],
            output_dir=str(output_dir),
            format="markdown",
            **({"hybrid": "docling-fast", "use_struct_tree": True} if not args.no_hybrid else {}),
        )
    finally:
        if server_proc is not None:
            server_proc.terminate()
            print("Hybrid server stopped.")

    md_path = output_dir / (pdf_path.stem + ".md")
    print(f"Done. To generate an index run in Claude Code:\n  /index-file {md_path}")


if __name__ == "__main__":
    main()
