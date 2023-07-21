FROM mcr.microsoft.com/devcontainers/python:3.10-bullseye

# Install Java
RUN apt update && \
    apt install -y sudo && \
    sudo apt install default-jdk -y

## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip
# Install production dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt