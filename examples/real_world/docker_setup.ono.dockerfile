FROM ubuntu:22.04
WORKDIR <?ono get appropriate working directory for containerized apps ?>
COPY requirements.txt .
RUN <?ono generate appropriate pip install command with security best practices ?>