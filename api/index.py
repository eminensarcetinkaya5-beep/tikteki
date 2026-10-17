from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

VPN_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusVPN - Ultra Secure Web Proxy & VPN</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #030712;
            --bg-card: rgba(17, 24, 39, 0.7);
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --border-color: rgba(255, 255, 255, 0.08);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-main); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; overflow-x: hidden; }

        .glow { position: fixed; border-radius: 50%; filter: blur(140px); z-index: -1; opacity: 0.2; }
        .glow-1 { top: -10%; left: -10%; width: 400px; height: 400px; background: var(--accent-blue); }
        .glow-2 { bottom: -10%; right: -10%; width: 400px; height: 400px; background: var(--accent-green); }

        .container { width: 100%; max-width: 480px; background: var(--bg-card); backdrop-filter: blur(20px); border: 1px solid var(--border-color); border-radius: 24px; padding: 35px; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5); text-align: center; animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

        .logo { font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 25px; display: flex; align-items: center; justify-content: center; gap: 10px; letter-spacing: -0.5px; }
        .logo i { color: var(--accent-green); text-shadow: 0 0 15px rgba(16,185,129,0.4); }

        /* Lokasyon Seçimi */
        .select-box { margin-bottom: 25px; text-align: left; }
        .select-box label { font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 8px; }
        select { width: 100%; padding: 14px 18px; border-radius: 14px; border: 1px solid var(--border-color); background: rgba(3, 7, 18, 0.8); color: #fff; font-size: 15px; outline: none; transition: all 0.3s; }
        select:focus { border-color: var(--accent-green); box-shadow: 0 0 15px rgba(16, 185, 129, 0.2); }

        /* Büyük Bağlantı Butonu */
        .connect-btn { width: 130px; height: 130px; border-radius: 50%; background: linear-gradient(135deg, #1f2937, #111827); border: 4px solid var(--border-color); color: var(--text-muted); font-size: 28px; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px auto; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .connect-btn i { font-size: 36px; margin-bottom: 5px; transition: color 0.3s; }
        .connect-btn span { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

        .connect-btn.active { background: linear-gradient(135deg, #059669, #10b981); border-color: #34d399; color: #fff; box-shadow: 0 0 40px rgba(16, 185, 129, 0.5); transform: scale(1.05); }
        .connect-btn.active i { color: #fff; text-shadow: 0 0 10px #fff; }

        /* Durum Kartı */
        .status-card { background: rgba(3, 7, 18, 0.6); border: 1px solid var(--border-color); border-radius: 16px; padding: 16px; display: flex; justify-content: space-around; align-items: center; margin-top: 25px; }
        .stat-item h4 { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 2px; }
        .stat-item p { font-size: 12px; color: var(--text-muted); text-transform: uppercase; }

        /* Proxy Web Arama Alanı */
        .proxy-box { margin-top: 25px; display: none; text-align: left; animation: fadeIn 0.4s ease-out; }
        .proxy-box input { width: 100%; padding: 12px 16px; border-radius: 12px; border: 1px solid var(--border-color); background: rgba(3, 7, 18, 0.9); color: #fff; font-size: 14px; outline: none; margin-bottom: 10px; }
        .proxy-box input:focus { border-color: var(--accent-blue); }
        .proxy-btn { width: 100%; padding: 12px; background: var(--accent-blue); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 14px; cursor: pointer; transition: background 0.3s; }
        .proxy-btn:hover { background: #2563eb; }
    </style>
</head>
<body>

    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div class="container">
        <div class="logo"><i class="fa-solid fa-shield-halated"></i> NexusVPN Pro</div>

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
            <i class="fa-solid fa-power-off"></i>
            <span id="btnText">Bağlan</span>
        </button>

        <p id="connectionStatus" style="font-size: 14px; color: var(--text-muted); font-weight: 600;">Güvenli tünel kapalı</p>

        <div class="status-card">
            <div class="stat-item">
                <h4 id="pingText">-- ms</h4>
                <p>Gecikme</p>
            </div>
            <div style="width:1px; height:30px; background:var(--border-color);"></div>
            <div class="stat-item">
                <h4 id="ipText">192.168.1.1</h4>
                <p>Sanal IP</p>
            </div>
        </div>

        <!-- Gizli Web Sörf Proxy Alanı -->
        <div class="proxy-box" id="proxyBox">
            <label style="font-size:12px; font-weight:700; color:var(--accent-blue); display:block; margin-bottom:6px;">ŞİFRELİ WEB SÖRFÜ</label>
            <input type="text" id="targetUrl" placeholder="https://ornek.com adresini girin...">
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
                btnText.textContent = "Bağlı";
                statusText.textContent = "256-bit AES Şifreleme Aktif 🔒";
                statusText.style.color = "var(--accent-green)";
                pingText.textContent = Math.floor(Math.random() * 20) + 12 + " ms";
                ipText.textContent = "185.220." + Math.floor(Math.random() * 200) + "." + Math.floor(Math.random() * 200);
                proxyBox.style.display = "block";
            } else {
                btn.classList.remove('active');
                btnText.textContent = "Bağlan";
                statusText.textContent = "Güvenli tünel kapalı";
                statusText.style.color = "var(--text-muted)";
                pingText.textContent = "-- ms";
                ipText.textContent = "192.168.1.1";
                proxyBox.style.display = "none";
            }
        }

        function launchProxy() {
            const url = document.getElementById('targetUrl').value.trim();
            if (!url) {
                alert('Lütfen geçerli bir web adresi girin!');
                return;
            }
            alert('NexusVPN Tüneli üzerinden yönlendiriliyor: ' + url);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(VPN_HTML_TEMPLATE)

@app.route('/api/status')
def status():
    return jsonify({'status': 'online', 'server': 'NexusVPN Cloud'})
    
