# Fabricio <last name> - Lab 3 Fibonacci Server
import socket
from flask import Flask, request

app = Flask(__name__)

@app.route("/register", methods=["PUT"])
def register():
    body = request.get_json(force=True, silent=True) or {}
    hostname, ip = body.get("hostname"), body.get("ip")
    as_ip, as_port = body.get("as_ip"), body.get("as_port")
    if not all([hostname, ip, as_ip, as_port]):
        return "missing fields", 400

    msg = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(msg.encode(), (as_ip, int(as_port)))
        sock.recvfrom(2048)
    except Exception:
        return "registration failed", 500
    return "registered", 201

@app.route("/fibonacci")
def fibonacci():
    try:
        x = int(request.args.get("number"))
        if x < 0:
            raise ValueError
    except (TypeError, ValueError):
        return "bad format", 400
    a, b = 0, 1
    for _ in range(x):
        a, b = b, a + b
    return str(a), 200

app.run(host="0.0.0.0", port=9090)
