# Lightweight Python image
FROM python:3.10-slim 

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

# Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Service's port
EXPOSE 8080

CMD ["python3", "-m", "openapi_server"]
