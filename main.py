import utime
import network
import socket
import ujson as json
from machine import Pin, ADC

SSID = 'iPhone - Chiriac'
PASS = '12345678'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASS)
while not wlan.isconnected():
    utime.sleep_ms(200)
print("IP:", wlan.ifconfig()[0])

pw = Pin(0, Pin.OUT)
wa = ADC(Pin(26))
ps = Pin(1, Pin.OUT)
sa = ADC(Pin(27))
pump = Pin(6, Pin.OUT)
led = Pin(15, Pin.OUT)

a3, a2, a1, a0 = (
    3.950844075038e-11,
    -1.8232912289820e-6,
    0.0279015,
    -131.227
)
MIN_WATER_PCT = 20.0
SOIL_TARGET = 40.0
LED_ON_THRESHOLD = 30.0
LED_OFF_THRESHOLD = 90.0

def raw2pct(r):
    p = ((a3*r + a2)*r + a1)*r + a0
    return max(0.0, min(100.0, p))

def read_w():
    pw.high()
    utime.sleep_ms(10)
    v = wa.read_u16()
    pw.low()
    return v

def read_s():
    ps.high()
    utime.sleep_ms(10)
    v = sa.read_u16()
    ps.low()
    return v

PAGE = f"""HTTP/1.0 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="ro">
<head><meta charset="utf-8"><title>Smart Pump</title>
<script src="https://cdn.jsdelivr.net/npm/canvas-gauges@2.1.7/gauge.min.js"></script>
<style>
 body {{ background:#1f2d3d;color:#fff;font-family:sans-serif;
        margin:0;display:flex;flex-direction:column;align-items:center }}
 header {{ padding:1em;font-size:2em;font-weight:bold }}
 #container {{ display:flex;gap:3em;margin-top:1em }}
 .box {{ text-align:center }}
 canvas {{ width:200px!important;height:auto!important }}
 button {{ margin:1em;padding:.8em 2em;font-weight:bold;
          background:#00aaff;color:#1f2d3d;border:none;border-radius:4px;
          cursor:pointer }}
 button:disabled {{ background:#555;cursor:not-allowed }}
</style>
</head>
<body>
  <header>Smart Pump</header>
  <div id="container">
    <div class="box"><canvas id="gaugeW"></canvas><div>Water %</div></div>
    <div class="box"><canvas id="gaugeS"></canvas><div>Soil %</div></div>
  </div>
  <button id="btn" disabled>Pornește pompa</button>
  <script>
    const MIN_W = {MIN_WATER_PCT}, SOIL_T = {SOIL_TARGET};
    const cfg = {{
      width:200,height:120,units:'%',minValue:0,maxValue:100,
      majorTicks:['0','20','40','60','80','100'],minorTicks:4,strokeTicks:true,
      highlights:[
        {{from:0,to:33,color:'rgba(255,67,39,0.6)'}},
        {{from:33,to:66,color:'rgba(255,215,0,0.6)'}},
        {{from:66,to:100,color:'rgba(14,230,255,0.6)'}}
      ],
      colorPlate:'#273447',colorMajorTicks:'#a1b5c9',
      colorMinorTicks:'#a1b5c9',colorNumbers:'#a1b5c9',
      borders:false,needleType:'arrow',needleWidth:4,
      needleCircleSize:8,needleCircleOuter:true,
      animationDuration:200
    }};
    const gW = new RadialGauge(Object.assign({{
      renderTo:'gaugeW',colorUnits:'#ff453f',colorNumbers:'#ff453f'
    }},cfg)).draw();
    const gS = new RadialGauge(Object.assign({{
      renderTo:'gaugeS',colorUnits:'#0ef',colorNumbers:'#0ef'
    }},cfg)).draw();
    const btn = document.getElementById('btn');
    let wasBelow = true;
    async function update() {{
      const res = await fetch('/data');
      const d = await res.json();
      gW.value = d.w_pct;
      gS.value = d.s_pct;
      if (d.w_pct < MIN_W) {{
        btn.disabled = true; wasBelow = true;
      }} else if (wasBelow && d.w_pct >= MIN_W) {{
        btn.disabled = false; wasBelow = false;
      }}
    }}
    btn.addEventListener('click', async () => {{
      btn.disabled = true; wasBelow = true;
      await fetch('/pump', {{ method:'POST' }});
    }});
    setInterval(update, 500);
    update();
  </script>
</body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print("Listening on http://%s:80" % wlan.ifconfig()[0])

led_on = False

while True:
    cl, _ = s.accept()
    req = cl.recv(1024)
    if not req:
        cl.close()
        continue
    method, path = req.split(b'\r\n', 1)[0].split()[:2]

    raw_w = read_w(); w_pct = raw2pct(raw_w)
    raw_s = read_s(); s_pct = 100 - raw_s * 100 / 65535

    if not led_on and w_pct < LED_ON_THRESHOLD:
        led.high()
        led_on = True
    elif led_on and w_pct > LED_OFF_THRESHOLD:
        led.low()
        led_on = False

    if s_pct >= SOIL_TARGET or w_pct <= MIN_WATER_PCT:
        pump.low()
    else:
        pump.high()

    if method == b'POST' and path == b'/pump':
        if w_pct >= MIN_WATER_PCT:
            pump.high(); utime.sleep(3); pump.low()
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type:application/json\r\n\r\n")
        cl.send(json.dumps({'ok': True}))
    elif path == b'/data':
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type:application/json\r\n\r\n")
        cl.send(json.dumps({'w_pct': w_pct, 's_pct': s_pct, 'pump': pump.value()}))
    else:
        cl.send(PAGE.encode())
    cl.close()
