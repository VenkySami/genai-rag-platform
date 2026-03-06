import argparse
from pathlib import Path

from app.ingestion.chunking import split_documents
from app.ingestion.pdf_loader import load_pdf
from app.vector_db.qdrant_client import create_vector_store


def parse_args() -> Path:
    parser = argparse.ArgumentParser(
        description="Ingest PDFs from a directory into the vector store."
    )
    parser.add_argument(
        "pdf_location",
        type=Path,
        help="Directory path containing PDF files (e.g. data/pdfs)",
    )
    args = parser.parse_args()
    location = args.pdf_location.resolve()
    if not location.is_dir():
        raise SystemExit(f"Not a directory: {location}")
    return location


def run_ingestion(location: Path) -> None:
    pdf_files = sorted(location.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {location}")
    docs = []
    for path in pdf_files:
        docs.extend(load_pdf(str(path)))
    chunks = split_documents(docs)
    create_vector_store(chunks)
    print("System Ready")


def main() -> None:
    location = parse_args()
    run_ingestion(location)


if __name__ == "__main__":
    main()
