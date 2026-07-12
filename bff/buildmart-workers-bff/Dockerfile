FROM python:3.11-slim

WORKDIR /usr/src/app/buildmart-workers-bff

COPY buildmart-workers-bff/ .
COPY common/ ./common/

RUN cp -r common/* ./ && rm -rf common && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x start.sh

EXPOSE 8102
CMD ["./start.sh"]
