dev:
	DYLD_LIBRARY_PATH=/opt/homebrew/lib uv run uvicorn app.main:app --reload

celery:
	DYLD_LIBRARY_PATH=/opt/homebrew/lib uv run celery -A app.celery_app worker --loglevel=info
