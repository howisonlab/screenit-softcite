FROM mcr.microsoft.com/devcontainers/python:3.10-bullseye

# Install Java
COPY apt.txt /tmp/
RUN apt update && \
    apt install -y sudo && \
    xargs -n 1 -- sudo apt install -y <  /tmp/apt.txt && \
    rm /tmp/apt.txt     
    
## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip
# Install production dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt