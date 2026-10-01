FROM python:3.12-slim
WORKDIR /app
RUN pip install flask
COPY . .
EXPOSE 9090
CMD ["python", "fs_server.py"]
