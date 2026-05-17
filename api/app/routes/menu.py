from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/menu", response_class=HTMLResponse)
def control_panel():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Irrigation Control</title>

<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
    background: #0f172a;
    color: white;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 500px;
    margin: auto;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

.zone {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
}

.zone-title {
    font-size: 18px;
    margin-bottom: 10px;
}

.status {
    font-size: 14px;
    margin-bottom: 10px;
    color: #94a3b8;
}

.buttons {
    display: flex;
    gap: 10px;
}

button {
    flex: 1;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: 0.2s;
}

.on {
    background: #22c55e;
    color: black;
}

.off {
    background: #ef4444;
    color: white;
}

.timed {
    background: #38bdf8;
    color: #082f49;
}

button:hover {
    opacity: 0.85;
}

.all-off {
    width: 100%;
    margin-top: 20px;
    background: #f97316;
    color: white;
    font-weight: bold;
}

.footer {
    text-align: center;
    margin-top: 15px;
    font-size: 12px;
    color: #64748b;
}
</style>
</head>

<body>
<div class="container">
    <h1>🌱 Irrigation Control</h1>

    <div id="zones"></div>

    <button class="all-off" onclick="allOff()">ALL OFF</button>

    <div class="footer">Live control via FastAPI</div>
</div>

<script>
const zones = [1, 2, 3, 4];

function renderZones(statusData) {
    const container = document.getElementById("zones");
    container.innerHTML = "";

    zones.forEach(z => {
        const isOn = statusData["zone" + z];

        container.innerHTML += `
            <div class="zone">
                <div class="zone-title">Zone ${z}</div>
                <div class="status">
                    Status: <b style="color:${isOn ? '#22c55e' : '#ef4444'}">
                    ${isOn ? 'ON' : 'OFF'}
                    </b>
                </div>
                <div class="buttons">
                    <button class="on" onclick="setZone(${z}, 'on')">ON</button>
                    <button class="timed" onclick="runZoneFor10Min(${z})">10 Min</button>
                    <button class="off" onclick="setZone(${z}, 'off')">OFF</button>
                </div>
            </div>
        `;
    });
}

async function fetchStatus() {
    try {
        const res = await fetch('/status');
        const data = await res.json();
        renderZones(data);
    } catch (err) {
        console.error("Status error:", err);
    }
}

async function setZone(zone, state) {
    try {
        await fetch(`/valve/${zone}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ state: state, source: 'menu' })
        });
        setTimeout(fetchStatus, 200);
    } catch (err) {
        console.error("Control error:", err);
    }
}

async function runZoneFor10Min(zone) {
    try {
        await fetch(`/valve/${zone}/10-min`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ source: 'menu' })
        });
        setTimeout(fetchStatus, 200);
    } catch (err) {
        console.error("10 minute run error:", err);
    }
}

async function allOff() {
    for (let z of zones) {
        await setZone(z, 'off');
    }
    fetchStatus();
}

// Initial load
fetchStatus();

// Auto refresh every 3 seconds
setInterval(fetchStatus, 3000);
</script>

</body>
</html>
"""
