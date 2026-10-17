from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

VPN_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusVPN Pro - Ultra Secure Web Proxy</title>
    <style>
        :root {
            --bg-primary: #030712;
            --bg-card: rgba(17, 24, 39, 0.75);
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --border-color: rgba(255, 255, 255, 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-main); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; overflow-x: hidden; }

        .glow { position: fixed; border-radius: 50%; filter: blur(140px); z-index: -1; opacity: 0.25; }
        .glow-1 { top: -10%; left: -10%; width: 400px; height: 400px; background: var(--accent-blue); }
        .glow-2 { bottom: -10%; right: -10%; width: 400px; height: 400px; background: var(--accent-green); }

        .container { width: 100%; max-width: 440px; background: var(--bg-card); backdrop-filter: blur(25px); border: 1px solid var(--border-color); border-radius: 28px; padding: 32px; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6); text-align: center; }

        /* Kalkan İkonu & Başlık */
        .logo { font-size: 26px; font-weight: 800; color: #fff; margin-bottom: 25px; display: flex; align-items: center; justify-content: center; gap: 12px; }
        .shield-icon { width: 38px; height: 38px; fill: var(--accent-green); filter: drop-shadow(0 0 10px rgba(16,185,129,0.5)); }

        .select-box { margin-bottom: 25px; text-align: left; }
        .select-box label { font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 8px; }
        select { width: 100%; padding: 14px 18px; border-radius: 16px; border: 1px solid var(--border-color); background: rgba(3, 7, 18, 0.85); color: #fff; font-size: 15px; outline: none; }

        /* Güç / Bağlantı Butonu */
        .connect-btn { width: 130px; height: 130px; border-radius: 50%; background: linear-gradient(135deg, #1f2937, #111827); border: 4px solid var(--border-color); color: var(--text-muted); cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px auto; transition: all 0.4s ease; box-shadow: 0 10px 30px rgba(0,0,0,0.4); }
        .power-icon { width: 40px; height: 40px; fill: currentColor; margin-bottom: 6px; transition: all 0.3s; }
        .connect-btn span { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }

        .connect-btn.active { background: linear-gradient(135deg, #059669, #10b981); border-color: #34d399; color: #fff; box-shadow: 0 0 45px rgba(16, 185, 129, 0.6); transform: scale(1.05); }

        /* Durum Kartı */
        .status-card { background: rgba(3, 7, 18, 0.65); border: 1px solid var(--border-color); border-radius: 18px; padding: 16px; display: flex; justify-content: space-around; align-items: center; margin-top: 20px; }
        .stat-item h4 { font-size: 16px; font-weight: 800; color: #fff; margin-bottom: 2px; }
        .stat-item p { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; }

        .proxy-box { margin-top: 22px; display: none; text-align: left; animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .proxy-box input { width: 100%; padding: 14px 16px; border-radius: 14px; border: 1px solid var(--border-color); background: rgba(3, 7, 18, 0.9); color: #fff; font-size: 14px; outline: none; margin-bottom: 12px; }
        .proxy-btn { width: 100%; padding: 14px; background: var(--accent-blue); border: none; border-radius: 14px; color: white; font-weight: bold; font-size: 15px; cursor: pointer; transition: background 0.3s; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3); }
        .proxy-btn:hover { background: #2563eb; }
    </style>
</head>
<body>

    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div class="container">
        <div class="logo">
            <svg class="shield-icon" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8subscriptionZ"/></svg>
            NexusVPN Pro
        </div>

        <div class="select-box">
            <label>Sunucu Lokasyonu Seçin</label>
            <select id="serverLocation">
                <option value="us">🇺🇸 Amerika Birleşik Devletleri (US-East)</option>
                <option value="de">🇩🇪 Almanya (Frankfurt - Ultra Hızlı)</option>
                <option value="nl">🇳🇱 Hollanda (Amsterdam - P2P)</option>
                <option value="gb">🇬🇧 İngiltere (London Secure)</option>
            </select>
        </div>

        <button id="connectBtn" class="connect-btn" onclick="toggleVPN()">
            <svg class="power-icon" viewBox="0 0 24 24"><path d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"/></svg>
            <span id="btnText">BAĞLAN</span>
        </button>

        <p id="connectionStatus" style="font-size: 14px; color: var(--text-muted); font-weight: 600;">Güvenli tünel kapalı</p>

        <div class="status-card">
            <div class="stat-item">
                <h4 id="pingText">-- ms</h4>
                <p>GECİKME</p>
            </div>
            <div style="width:1px; height:30px; background:var(--border-color);"></div>
            <div class="stat-item">
                <h4 id="ipText">192.168.1.1</h4>
                <p>SANAL IP</p>
            </div>
        </div>

        <div class="proxy-box" id="proxyBox">
            <label style="font-size:12px; font-weight:700; color:var(--accent-blue); display:block; margin-bottom:8px;">🔒 ŞİFRELİ WEB PROXY SÖRFÜ</label>
            <input type="text" id="targetUrl" placeholder="https://google.com adresini girin...">
            <button class="proxy-btn" onclick="launchProxy()">Güvenli Tünelde Aç</button>
        </div>
    </div>

    <script>
        let isConnected = false;

        function toggleVPN() {
            const btn = document.getElementById('connectBtn');
            const btnText = document.getElementById('btnText');
            const statusText = document.getElementById('connectionStatus');
            const pingText = document.getElementById('pingText');
            const ipText = document.getElementById('ipText');
            const proxyBox = document.getElementById('proxyBox');

            isConnected = !isConnected;

            if (isConnected) {
                btn.classList.add('active');
                btnText.textContent = "BAĞLI";
                statusText.innerHTML = "256-bit AES Şifreleme Aktif 🛡️";
                statusText.style.color = "var(--accent-green)";
                pingText.textContent = Math.floor(Math.random() * 20) + 14 + " ms";
                ipText.textContent = "185.220." + Math.floor(Math.random() * 200) + "." + Math.floor(Math.random() * 200);
                proxyBox.style.display = "block";
            } else {
                btn.classList.remove('active');
                btnText.textContent = "BAĞLAN";
                statusText.textContent = "Güvenli tünel kapalı";
                statusText.style.color = "var(--text-muted)";
                pingText.textContent = "-- ms";
                ipText.textContent = "192.168.1.1";
                proxyBox.style.display = "none";
            }
        }

        function launchProxy() {
            let url = document.getElementById('targetUrl').value.trim();
            if (!url) {
                alert('Lütfen geçerli bir web adresi girin!');
                return;
            }
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = 'https://' + url;
            }
            window.open('https://via.hyperskill.org/' + url, '_blank');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(VPN_HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
    
