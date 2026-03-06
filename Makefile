.PHONY: install test run-ingestion run-api lint

install:
	poetry install
	poetry run ruff check .

test:
	@echo "No tests configured."

PDF_DIR ?= data/pdfs
run-ingestion:
	poetry run python main.py "$(PDF_DIR)"

run-api:
	poetry run uvicorn api.chatbot:api --reload --host 0.0.0.0 --port 8000
