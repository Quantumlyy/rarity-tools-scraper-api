alembic upgrade head

python -m uvicorn rarity_tools_scraper_api.main:app --host 0.0.0.0 --port 80
