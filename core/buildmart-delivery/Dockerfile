FROM python:3.11-slim

WORKDIR /usr/src/app/buildmart-delivery

COPY buildmart-delivery/ .
COPY common/ ./common/

RUN cp -r common/* ./ && rm -rf common && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x start.sh

EXPOSE 8003
CMD ["./start.sh"]
