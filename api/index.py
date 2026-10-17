from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTeki - Ultimate Live Studio</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: #05070f; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: rgba(20, 30, 55, 0.8); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
        h1 { color: #ff0050; margin-bottom: 10px; }
        p { color: #94a3b8; }
    </style>
</head>
<body>
    <div class="card">
        <h1><i class="fa-solid fa-bolt"></i> TikTeki Aktif!</h1>
        <p>Sistem ve Vercel bağlantısı başarıyla kuruldu.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/check-live')
def check_live():
    username = request.args.get('username', '').replace('@', '').strip()
    if not username:
        return jsonify({'status': 'not_found'})
    try:
        from TikTokLive import TikTokLiveClient
        client = TikTokLiveClient(unique_id=username)
        if not client.is_live():
            return jsonify({'status': 'offline'})
        return jsonify({'status': 'online'})
    except Exception:
        return jsonify({'status': 'not_found'})
        
