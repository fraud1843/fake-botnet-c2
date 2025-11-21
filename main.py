#!/usr/bin/env python3
import http.server
import socketserver
import threading
import random
import time
import json
from datetime import datetime

PORT = 9977
bots = {}

def fake_bot_generator():
    while True:
        time.sleep(random.randint(3,15))
        bot_id = random.choice(["WIN-", "LNX-", "MAC-"]) + hex(random.randint(0x100000,0xffffff))[2:].upper()
        ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        country = random.choice(["US","RU","CN","BR","DE","FR","IN","KR","UA","NL"])
        version = "1.3.37"
        last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        bots[bot_id] = {"ip":ip,"country":country,"version":version,"last":last}
        if len(bots) > 500:
            del bots[random.choice(list(bots.keys()))]

threading.Thread(target=fake_bot_generator, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Zeus v2.1.0.1</title>
  <meta charset="utf-8">
  <style>
    body {background:#111; color:#0f0; font-family:'Courier New';}
    table {width:100%; border-collapse:collapse; margin-top:20px;}
    th, td {border:1px solid #0f0; padding:8px; text-align:left;}
    th {background:#003300;}
    .header {font-size:2em; text-align:center; margin:20px;}
    .stats {font-size:1.5em; margin:20px;}
  </style>
</head>
<body>
  <div class="header">♛ Zeus Panel v2.1.0.1 ♛</div>
  <div class="stats">Online Bots: <span id="cnt">0</span> │ Loader Active │ Uptime 1337h 37m</div>
  
  <table>
    <tr><th>ID</th><th>IP Address</th><th>Country</th><th>Version</th><th>Last Seen</th></tr>
    <tbody id="bots"></tbody>
  </table>

<script>
function update() {
  fetch('/bots').then(r => r.json()).then(data => {
    document.getElementById('cnt').innerText = data.length;
    let html = '';
    data.forEach(b => {
      html += `<tr><td>${b.id}</td><td>${b.ip}</td><td>${b.country}</td><td>${b.version}</td><td>${b.last}</td></tr>`;
    });
    document.getElementById('bots').innerHTML = html;
  });
}
setInterval(update, 3000);
update();
</script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path == '/bots':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            botlist = [{"id":k, "ip":v["ip"], "country":v["country"], "version":v["version"], "last":v["last"]} for k,v in bots.items()]
            self.wfile.write(json.dumps(botlist).encode())
        else:
            self.send_response(404)
            self.end_headers()

print(f"[+] Fake Zeus C2 starting on port {PORT}")
print(f"[+] Visit http://YOUR_VPS_IP:{PORT}/ when it's up")
print(f"[+] Bots will start appearing automatically")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
