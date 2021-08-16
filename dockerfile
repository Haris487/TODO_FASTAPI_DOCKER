# Pull base image
FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN python -V
RUN pip -V
COPY . /code/
RUN pip install -r requirements.txt


EXPOSE 8000