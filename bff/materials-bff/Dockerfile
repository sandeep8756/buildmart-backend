FROM python:3.11-slim
WORKDIR /app
COPY bff/materials-bff/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bff/materials-bff/ /app/
EXPOSE 8101
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8101"]
