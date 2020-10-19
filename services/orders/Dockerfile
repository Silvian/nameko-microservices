FROM python:3.8

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
WORKDIR "usr/src/services/orders"

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . /usr/src/services/orders

# Run the app
CMD ["./services/orders/run_services.sh"]
