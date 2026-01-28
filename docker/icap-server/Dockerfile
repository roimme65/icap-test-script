FROM python:3.11-alpine

WORKDIR /app

# Copy ICAP server
COPY icap_server.py .

# Expose ICAP port
EXPOSE 1344

# Run server
CMD ["python3", "icap_server.py"]
