import json
import socket
import struct
import time

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
    sock.settimeout(2.0)
    try:
        packet = b'SAMP' + socket.inet_aton(ip) + struct.pack('<H', int(port)) + b'i'
        sock.sendto(packet, (ip, int(port)))
        data, _ = sock.recvfrom(1024)
        if len(data) >= 16:
            online, max_players = struct.unpack('<HH', data[12:16])
            return str(online), str(max_players)
    except Exception:
        pass
    finally:
        sock.close()
    return None

print("Скрипт мониторинга запущен. Обновление каждые 10 секунд...")

while True:
    try:
        for srv in servers:
            res = query_samp(srv["ip"], srv["port"])
            if res:
                srv["online"], srv["maxonline"] = res
            else:
                # Если сервер выключен или не отвечает, сбрасываем онлайн в 0
                srv["online"] = "0"

        with open("servers.json", "w", encoding="utf-8") as f:
            json.dump(servers, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Ошибка в цикле обновления: {e}")

    time.sleep(10)
