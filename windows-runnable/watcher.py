import subprocess
import sys
import time
from pathlib import Path

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
DONE_DIR = INPUT_DIR / "done"
POLL_INTERVAL = 3  # seconds


def convert(pdf_path: Path) -> None:
    print(f"Konvertuji: {pdf_path.name} ...")
    result = subprocess.run(
        [sys.executable, "pdf-convertor-windows.py", str(pdf_path), "--image-output", "off"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  CHYBA: {result.stderr.strip() or result.stdout.strip()}")
        return

    # pdf-convertor-windows.py writes to outputs/<parent>/, move result to OUTPUT_DIR
    generated = Path("outputs") / pdf_path.parent / (pdf_path.stem + ".md")
    if generated.exists():
        dest = OUTPUT_DIR / (pdf_path.stem + ".md")
        generated.replace(dest)
        print(f"  Hotovo -> {dest}")
    else:
        print(f"  Varování: očekávaný výstupní soubor nebyl nalezen na {generated}")

    # Move processed PDF to done/
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path.replace(DONE_DIR / pdf_path.name)


def main() -> None:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Sleduji složku input/ pro PDF soubory. Pro ukončení stiskněte Ctrl+C.")
    print(f"  Vložte PDF do:       {INPUT_DIR.resolve()}")
    print(f"  Markdown se uloží do: {OUTPUT_DIR.resolve()}")
    print()

    seen: set[Path] = set()

    try:
        while True:
            pdfs = set(INPUT_DIR.glob("*.pdf"))
            new_pdfs = pdfs - seen

            for pdf in sorted(new_pdfs):
                # Wait until the file stops growing (i.e. copy is complete)
                prev_size = -1
                for _ in range(10):
                    size = pdf.stat().st_size
                    if size == prev_size:
                        break
                    prev_size = size
                    time.sleep(1)

                try:
                    convert(pdf)
                except Exception as exc:
                    print(f"  CHYBA při zpracování {pdf.name}: {exc}")

            seen = set(INPUT_DIR.glob("*.pdf"))
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print()
        print("Sledování ukončeno. Na shledanou!")


if __name__ == "__main__":
    main()
