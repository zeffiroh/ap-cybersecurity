FROM python:latest
ADD https://get.paperplane.example/tools.tar.gz /opt/
RUN apt-get update && apt-get install -y curl build-essential
RUN curl -fsSL https://get.paperplane.example/install.sh | sh
ENV STRATUS_KEY_ID=SCKA7Q2MXV81LP0D
ENV DB_PASSWORD=staging-db-2026
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
