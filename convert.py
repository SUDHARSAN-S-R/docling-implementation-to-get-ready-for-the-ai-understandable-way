from pathlib import Path
import json

from docling.document_converter import DocumentConverter


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DOCLING CONVERTER
# ============================================================

converter = DocumentConverter()


# ============================================================
# PROCESS ONE DOCUMENT
# ============================================================

def process_document(file_path: Path):

    print()
    print("=" * 70)
    print(f"PROCESSING: {file_path.name}")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: INPUT
    # --------------------------------------------------------

    print("\n[STEP 1] Input")
    print(f"File       : {file_path.name}")
    print(f"Extension  : {file_path.suffix.lower()}")

    # --------------------------------------------------------
    # STEP 2: DOCLING
    # --------------------------------------------------------

    print("\n[STEP 2] Docling conversion")

    result = converter.convert(file_path)

    print("Docling conversion completed.")

    # --------------------------------------------------------
    # STEP 3: NATIVE TEXT / OCR
    # --------------------------------------------------------

    print("\n[STEP 3] Native text / OCR")

    # Docling internally decides how to process the document.
    #
    # Normal PDF:
    #     native PDF text can be extracted.
    #
    # Scanned PDF / image:
    #     OCR can be used.
    #
    # We don't manually create PDF page images here.

    print("Native text/OCR processing completed.")

    # --------------------------------------------------------
    # STEP 4: STRUCTURED DOCUMENT
    # --------------------------------------------------------

    print("\n[STEP 4] Structured document")

    document = result.document

    print("DoclingDocument created.")

    # --------------------------------------------------------
    # STEP 5: MARKDOWN OUTPUT
    # --------------------------------------------------------

    print("\n[STEP 5] Markdown")

    markdown = document.export_to_markdown()

    markdown_file = OUTPUT_DIR / f"{file_path.stem}.md"

    markdown_file.write_text(
        markdown,
        encoding="utf-8"
    )

    print(f"Markdown saved: {markdown_file}")

    # --------------------------------------------------------
    # STEP 6: JSON OUTPUT
    # --------------------------------------------------------

    print("\n[STEP 6] JSON")

    json_data = document.export_to_dict()

    json_file = OUTPUT_DIR / f"{file_path.stem}.json"

    json_file.write_text(
        json.dumps(
            json_data,
            indent=2,
            ensure_ascii=False,
            default=str
        ),
        encoding="utf-8"
    )

    print(f"JSON saved: {json_file}")

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    print("\n[PREVIEW]")

    print(markdown[:2000])

    print()
    print("=" * 70)
    print(f"COMPLETED: {file_path.name}")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    if not INPUT_DIR.exists():
        print(f"Input directory does not exist: {INPUT_DIR}")
        return

    files = [
        file
        for file in INPUT_DIR.iterdir()
        if file.is_file()
    ]

    if not files:
        print("No files found in input directory.")
        return

    print("=" * 70)
    print("DOCLING DOCUMENT PIPELINE")
    print("=" * 70)

    print(f"\nFound {len(files)} input file(s).")

    for file_path in files:

        try:
            process_document(file_path)

        except Exception as error:

            print()
            print("!" * 70)
            print(f"ERROR processing: {file_path.name}")
            print(f"Error: {error}")
            print("!" * 70)


if __name__ == "__main__":
    main()