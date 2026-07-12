FROM python:3.11-slim
WORKDIR /app
COPY bff/delivery-bff/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bff/delivery-bff/ /app/
EXPOSE 8103
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8103"]
