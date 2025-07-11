SOLARA_APP=src/webapp.py uv run uvicorn --workers 4 --host 0.0.0.0 --port 8765 solara.server.starlette:app
