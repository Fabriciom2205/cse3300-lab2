# Fabricio <last name> - Lab 3 Authoritative Server
import socket, json, os

DB_FILE = "dns_records.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def parse(msg):
    # turns "TYPE=A\nNAME=x VALUE=y TTL=10" into a dict
    fields = {}
    for token in msg.split():
        if "=" in token:
            k, v = token.split("=", 1)
            fields[k.upper()] = v
    return fields

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 53533))
print("AS listening on UDP 53533")

while True:
    data, addr = sock.recvfrom(2048)
    f = parse(data.decode())
    db = load_db()
    name, rtype = f.get("NAME"), f.get("TYPE", "A")

    if "VALUE" in f:  # registration
        db[name] = {"TYPE": rtype, "VALUE": f["VALUE"], "TTL": f.get("TTL", "10")}
        save_db(db)
        r = db[name]
        reply = f"TYPE={rtype}\nNAME={name} VALUE={r['VALUE']} TTL={r['TTL']}\n"
    elif name in db:  # DNS query
        r = db[name]
        reply = f"TYPE={r['TYPE']}\nNAME={name} VALUE={r['VALUE']} TTL={r['TTL']}\n"
    else:
        reply = "NOT FOUND\n"
    sock.sendto(reply.encode(), addr)
