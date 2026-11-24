import json
import socket
import struct

servers = [
    {
        "logo": "moscow", "id": "1", "status": "", "online": "0", "maxonline": "100",
        "color": "FF0000", "x2": "false", "key": "1424", "name": "",
        "firstname": "DARK", "secondname": "", "url": "moscow.blackrussia.online",
        "ip": "80.242.59.112", "port": "2805"
    },
    {
        "logo": "moscow", "id": "2", "status": "", "online": "0", "maxonline": "100",
        "color": "FF0000", "x2": "false", "key": "1424", "name": "",
        "firstname": "TEST-1", "secondname": "", "url": "moscow.blackrussia.online",
        "ip": "188.127.241.74", "port": "2211"
    }
]

def query_samp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)
    try:
        packet = b'SAMP' + socket.inet_aton(ip) + struct.pack('<H', int(port)) + b'i'
        sock.sendto(packet, (ip, int(port)))
        data, _ = sock.recvfrom(1024)
        if len(data) >= 16:
            online, max_players = struct.unpack('<HH', data[12:16])
            return str(online), str(max_players)
    except Exception as e:
        print(f"Ошибка опроса {ip}:{port} -> {e}")
    finally:
        sock.close()
    return None

for srv in servers:
    res = query_samp(srv["ip"], srv["port"])
    if res:
        srv["online"], srv["maxonline"] = res
        print(f"{srv['firstname']}: {srv['online']}/{srv['maxonline']}")
    else:
        srv["online"] = "0"
        print(f"{srv['firstname']}: не отвечает (0)")

with open("servers.json", "w", encoding="utf-8") as f:
    json.dump(servers, f, indent=4, ensure_ascii=False)
