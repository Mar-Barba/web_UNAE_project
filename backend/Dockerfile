FROM python:3.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend

ENV PATH="/backend/.venv/bin:$PATH"

ENV PYTHONPATH=/backend

COPY "pyproject.toml" "uv.lock"  ./

RUN uv sync --locked --no-cache  --no-dev

COPY  "database/" ./database/

COPY "main.py"  ./

EXPOSE 18462

CMD ["gunicorn", "--bind", "0.0.0.0:18462", "main:app"]
