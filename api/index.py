from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTeki - Canlı Yayın Asistanı</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .card { background: #1e293b; border-radius: 20px; padding: 32px; width: 100%; max-width: 480px; box-shadow: 0 20px 30px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }
        .logo { font-size: 36px; font-weight: 900; background: linear-gradient(45deg, #ff0050, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; letter-spacing: -1px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
        .input-group { margin-bottom: 20px; text-align: left; }
        label { font-size: 12px; font-weight: 700; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.5px; }
        input { width: 100%; padding: 14px; margin-top: 6px; border-radius: 12px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 16px; outline: none; transition: 0.3s; }
        input:focus { border-color: #ff0050; box-shadow: 0 0 10px rgba(255, 0, 80, 0.3); }
        button { width: 100%; padding: 15px; background: linear-gradient(45deg, #ff0050, #00f2fe); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; }
        button:hover { opacity: 0.95; transform: scale(0.99); }
        .status { margin-top: 20px; padding: 14px; border-radius: 10px; font-size: 14px; background: #0f172a; border: 1px solid #334155; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">TikTeki</div>
        <p>TikTok Canlı Yayın Etkileşim & Overlay Paneli</p>
        <div class="input-group">
            <label>TikTok Kullanıcı Adı</label>
            <input type="text" id="username" placeholder="@kullanici_adi" value="@">
        </div>
        <button onclick="connectLive()">YAYINA BAĞLAN</button>
        <div id="status" class="status"></div>
    </div>

    <script>
        function connectLive() {
            const username = document.getElementById('username').value;
            const status = document.getElementById('status');
            if(!username || username === '@') {
                alert('Lütfen geçerli bir kullanıcı adı girin!');
                return;
            }
            status.style.display = 'block';
            status.innerHTML = '⚡ <b>' + username + '</b> yayınına TikTeki bağlanıyor...';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
  
