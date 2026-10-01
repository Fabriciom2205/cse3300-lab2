FROM python:3.12-slim
WORKDIR /app
RUN pip install flask requests
COPY . .
EXPOSE 8080
CMD ["python", "us_server.py"]
