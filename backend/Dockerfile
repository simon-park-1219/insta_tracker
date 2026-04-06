FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings \
    "python-jose[cryptography]" bcrypt python-multipart apscheduler aiosmtplib httpx email-validator

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
