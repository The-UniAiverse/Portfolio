FROM python:3.12-slim
# Bun runs the vendored ai-job-search job connector (app/services/jobs).
COPY --from=oven/bun:1.2 /usr/local/bin/bun /usr/local/bin/bun
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# Hosts like Render and Railway set $PORT; locally and in docker compose it falls back to 8000.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
