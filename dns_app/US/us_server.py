# Fabricio <last name> - Lab 3 User Server
import socket
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/fibonacci")
def fibonacci():
    keys = ["hostname", "fs_port", "number", "as_ip", "as_port"]
    p = {k: request.args.get(k) for k in keys}
    if not all(p.values()):
        return "bad request", 400

    # ask the AS for the IP of the hostname
    query = f"TYPE=A\nNAME={p['hostname']}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(query.encode(), (p["as_ip"], int(p["as_port"])))
        reply, _ = sock.recvfrom(2048)
    except Exception:
        return "could not reach AS", 500

    fs_ip = None
    for token in reply.decode().split():
        if token.startswith("VALUE="):
            fs_ip = token.split("=", 1)[1]
    if not fs_ip:
        return "hostname not found", 404

    # ask the FS for the answer
    r = requests.get(f"http://{fs_ip}:{p['fs_port']}/fibonacci",
                     params={"number": p["number"]})
    return r.text, r.status_code

app.run(host="0.0.0.0", port=8080)
