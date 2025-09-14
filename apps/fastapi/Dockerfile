FROM python:3.11.3 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.11.3-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
CMD ["/app/.venv/bin/fastapi", "run"]
# Make port 8000 available to the world outside the container
#EXPOSE 8000

# Run the application with Uvicorn, binding to all interfaces
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]