FROM python:3.11-slim
WORKDIR /app
COPY bff/workers-bff/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bff/workers-bff/ /app/
EXPOSE 8102
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8102"]
