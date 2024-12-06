# FROM python:3-alpine

# Testing with lightweight Python image
FROM python:3.10-slim 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

# Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Service's port
EXPOSE 8082

CMD ["python3", "-m", "openapi_server"]