FROM python:3.11-slim

WORKDIR /usr/src/app/buildmart-workers

COPY buildmart-workers/ .
COPY common/ ./common/

RUN cp -r common/* ./ && rm -rf common && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x start.sh

EXPOSE 8002
CMD ["./start.sh"]
