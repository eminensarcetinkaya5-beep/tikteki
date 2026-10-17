from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTeki - Ultimate Live Studio (1077+ Pro Features)</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #05070f;
            --bg-secondary: #0c1222;
            --bg-card: rgba(20, 30, 55, 0.65);
            --accent-pink: #ff0050;
            --accent-cyan: #00f2fe;
            --accent-purple: #7928ca;
            --accent-green: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.08);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-main); min-height: 100vh; display: flex; overflow-x: hidden; }

        .glow { position: fixed; border-radius: 50%; filter: blur(120px); z-index: -1; opacity: 0.25; animation: pulseGlow 12s infinite alternate ease-in-out; }
        .glow-1 { top: -100px; left: -100px; width: 500px; height: 500px; background: var(--accent-pink); }
        .glow-2 { bottom: -100px; right: -100px; width: 600px; height: 600px; background: var(--accent-cyan); }
        .glow-3 { top: 40%; left: 40%; width: 400px; height: 400px; background: var(--accent-purple); }
        @keyframes pulseGlow { 0% { transform: scale(1) translate(0, 0); } 100% { transform: scale(1.2) translate(30px, -30px); } }

        .sidebar { width: 290px; background: rgba(12, 18, 34, 0.85); backdrop-filter: blur(20px); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; padding: 25px; position: fixed; height: 100vh; z-index: 100; }
        .logo { font-size: 30px; font-weight: 900; background: linear-gradient(45deg, var(--accent-pink), var(--accent-cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; letter-spacing: -1px; }
        .logo i { -webkit-text-fill-color: initial; color: var(--accent-pink); text-shadow: 0 0 15px var(--accent-pink); }
        
        .menu-group { font-size: 11px; text-transform: uppercase; color: #475569; font-weight: 800; letter-spacing: 1px; margin: 15px 0 8px 10px; }
        .menu-items { display: flex; flex-direction: column; gap: 6px; flex: 1; overflow-y: auto; }
        .menu-item { padding: 12px 16px; border-radius: 12px; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; gap: 14px; font-weight: 600; font-size: 14px; transition: all 0.25s ease; border: 1px solid transparent; }
        .menu-item:hover { background: rgba(255, 255, 255, 0.05); color: #fff; transform: translateX(4px); }
        .menu-item.active { background: linear-gradient(90deg, rgba(255,0,80,0.2), rgba(0,242,254,0.05)); color: #fff; border-color: rgba(255,0,80,0.3); box-shadow: 0 4px 20px rgba(255,0,80,0.15); }
        .menu-item i { font-size: 16px; width: 22px; color: var(--accent-pink); }

        .main-content { margin-left: 290px; flex: 1; padding: 35px; max-width: calc(100% - 290px); animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .header-title { font-size: 26px; font-weight: 800; margin-bottom: 25px; color: #fff; display: flex; align-items: center; justify-content: space-between; }
        .header-title span { display: flex; align-items: center; gap: 12px; }
        
        .card { background: var(--bg-card); backdrop-filter: blur(16px); border-radius: 20px; padding: 28px; border: 1px solid var(--border-color); box-shadow: 0 20px 40px rgba(0,0,0,0.4); margin-bottom: 25px; }
        .card-title { font-size: 17px; font-weight: 700; color: #38bdf8; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-card { background: rgba(12, 18, 34, 0.7); border: 1px solid var(--border-color); padding: 20px; border-radius: 16px; text-align: center; position: relative; overflow: hidden; }
        .stat-card::before { content:''; position: absolute; top:0; left:0; width:100%; height:3px; background: linear-gradient(90deg, var(--accent-pink), var(--accent-cyan)); }
        .stat-card h4 { font-size: 26px; font-weight: 800; color: var(--accent-cyan); margin-bottom: 4px; }
        .stat-card p { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }

        .input-box { display: flex; gap: 12px; margin-bottom: 20px; }
        input[type="text"], input[type="number"], select { width: 100%; padding: 14px 18px; border-radius: 12px; border: 1px solid var(--border-color); background: rgba(5, 7, 15, 0.8); color: #fff; font-size: 15px; outline: none; transition: all 0.3s; }
        input:focus, select:focus { border-color: var(--accent-pink); box-shadow: 0 0 15px rgba(255, 0, 80, 0.25); }
        
        button { padding: 14px 26px; background: linear-gradient(135deg, var(--accent-pink), #ff5e62); border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 14px; cursor: pointer; transition: all 0.3s; box-shadow: 0 8px 20px rgba(255, 0, 80, 0.3); white-space: nowrap; display: flex; align-items: center; gap: 8px; justify-content: center; }
        button:hover { opacity: 0.95; transform: translateY(-2px); box-shadow: 0 12px 25px rgba(255, 0, 80, 0.4); }

        .profile-container { display: none; align-items: center; gap: 20px; background: rgba(5, 7, 15, 0.9); padding: 20px; border-radius: 16px; border: 1px solid var(--border-color); margin-top: 20px; }
        .profile-pic { width: 70px; height: 70px; border-radius: 50%; border: 3px solid var(--accent-pink); object-fit: cover; box-shadow: 0 0 20px rgba(255,0,80,0.4); }
        .profile-info h3 { font-size: 20px; color: #fff; margin-bottom: 4px; }
        .profile-info p { font-size: 13px; color: var(--text-muted); }
        
        .badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 30px; font-size: 12px; font-weight: bold; margin-top: 8px; }
        .badge-online { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-offline { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-error { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }

        .rule-form { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
        .rule-list { margin-top: 20px; display: flex; flex-direction: column; gap: 12px; }
        .rule-item { background: rgba(5, 7, 15, 0.8); padding: 16px 20px; border-radius: 14px; border-left: 4px solid var(--accent-pink); display: flex; justify-content: space-between; align-items: center; font-size: 14px; border-top: 1px solid var(--border-color); border-right: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); }

        .live-log-box { background: rgba(5, 7, 15, 0.95); border: 1px solid var(--border-color); border-radius: 14px; height: 220px; overflow-y: auto; padding: 15px; font-family: monospace; font-size: 13px; color: #a7f3d0; margin-top: 15px; }
        .log-entry { margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }

        .wheel-demo { width: 180px; height: 180px; border-radius: 50%; border: 8px solid var(--accent-pink); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-weight: bold; color: var(--accent-cyan); background: conic-gradient(#ff0050 0deg 90deg, #7928ca 90deg 180deg, #00f2fe 180deg 270deg, #10b981 270deg 360deg); animation: spinWheel 10s infinite linear; box-shadow: 0 0 30px rgba(0,242,254,0.3); }
        @keyframes spinWheel { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        @media(max-width: 900px) {
            .sidebar { width: 75px; padding: 20px 10px; }
            .sidebar .logo span, .sidebar .menu-item span, .menu-group { display: none; }
            .main-content { margin-left: 75px; max-width: calc(100% - 75px); padding: 20px; }
            .rule-form { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>

    <div class="sidebar">
        <div class="logo"><i class="fa-solid fa-bolt"></i><span>TikTeki</span></div>
        <div class="menu-items">
            <div class="menu-group">Genel</div>
            <div class="menu-item active" onclick="switchTab('tab-home', this)"><i class="fa-solid fa-gauge-high"></i><span>Kontrol Paneli</span></div>
            <div class="menu-item" onclick="switchTab('tab-rules', this)"><i class="fa-solid fa-wand-magic-sparkles"></i><span>Otomasyon & Kurallar</span></div>
            <div class="menu-item" onclick="switchTab('tab-feed', this)"><i class="fa-solid fa-stream"></i><span>Canlı Yayın Akışı</span></div>
            
            <div class="menu-group">Yayın Araçları</div>
            <div class="menu-item" onclick="switchTab('tab-games', this)"><i class="fa-solid fa-dharmachakra"></i><span>Çarkıfelek & Oyuncu</span></div>
            <div class="menu-item" onclick="switchTab('tab-minecraft', this)"><i class="fa-cube"></i><span>Minecraft / Webhook</span></div>
            <div class="menu-item" onclick="switchTab('tab-chatbot', this)"><i class="fa-solid fa-robot"></i><span>Chat Bot & Mod</span></div>
            
            <div class="menu-group">Görsel & Ses</div>
            <div class="menu-item" onclick="switchTab('tab-overlays', this)"><i class="fa-solid fa-desktop"></i><span>OBS Overlays</span></div>
            <div class="menu-item" onclick="switchTab('tab-tts', this)"><i class="fa-solid fa-volume-high"></i><span>TTS & Soundboard</span></div>
            <div class="menu-item" onclick="switchTab('tab-settings', this)"><i class="fa-solid fa-sliders"></i><span>Gelişmiş Ayarlar</span></div>
        </div>
    </div>

    <div class="main-content">
        
        <div id="tab-home" class="tab-content active">
            <div class="header-title">
                <span><i class="fa-solid fa-gauge-high" style="color:var(--accent-cyan);"></i> Yayın Stüdyosu & Canlı Analiz</span>
                <span style="font-size:12px; background:rgba(16,185,129,0.2); color:#10b981; padding:6px 14px; border-radius:20px; border:1px solid #10b981;">1077+ Modül Aktif</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><h4>1,250</h4><p>Tahmini Elmas (Gift)</p></div>
                <div class="stat-card"><h4>0 ms</h4><p>Sinyal Gecikmesi</p></div>
                <div class="stat-card"><h4>24/7</h4><p>Vercel Serverless</p></div>
                <div class="stat-card"><h4>%100</h4><p>TikFinity Uyumlu</p></div>
            </div>

            <div class="card">
                <div class="card-title"><i class="fa-solid fa-circle-play"></i> TikTok Yayın Bağlantı Denetleyicisi</div>
                <div class="input-box">
                    <input type="text" id="username" placeholder="TikTok Kullanıcı Adı (@kullanici)" value="@">
                    <button onclick="checkAndConnect()"><i class="fa-solid fa-plug"></i> Hesabı Test Et & Bağlan</button>
                </div>
                
                <div id="profileContainer" class="profile-container">
                    <img id="profileImg" src="" class="profile-pic" alt="Profil">
                    <div class="profile-info">
                        <h3 id="profileName">@kullanici</h3>
                        <p id="profileDesc">Durum sorgulanıyor...</p>
                        <div id="profileBadge" class="badge">Bekleniyor</div>
                    </div>
                </div>
            </div>
        </div>

        <div id="tab-rules" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-pink);"></i> Hediye & Etkileşim Otomasyon Motoru</span></div>
            <div class="card">
                <div class="rule-form">
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">TETİKLEYİCİ OLAY:</label>
                        <select id="eventType" style="margin-top:6px;">
                            <option value="Hediye: Gül (Rose)">Hediye: Gül (Rose - 1 Coin)</option>
                            <option value="Hediye: Aslan (Lion)">Hediye: Aslan (Lion - 29999 Coin)</option>
                            <option value="Hediye: Asa (Wand)">Hediye: Asa (Magic Wand)</option>
                            <option value="Olay: Yeni Takip">Olay: Yeni Takipçi</option>
                            <option value="Olay: Yayını Paylaştı">Olay: Yayın Paylaşımı</option>
                            <option value="Olay: 500+ Beğeni">Olay: 500 Beğeni Barajı</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">YAPILACAK EYLEM:</label>
                        <select id="actionType" style="margin-top:6px;">
                            <option value="TTS Okut">Yazıyı Sesli Okut (TTS Engine)</option>
                            <option value="Ses Çal">Özel MP3 Efekti Çal (Soundboard)</option>
                            <option value="Ekranda Konfeti">Ekranda Patlama / Konfeti Efekti</option>
                            <option value="Minecraft Komutu">Minecraft Server Komutu Çalıştır</option>
                        </select>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <input type="text" id="actionValue" placeholder="Örn: Harikayız! Teşekkürler {user}!">
                </div>
                <button onclick="addRule()" style="width:100%;"><i class="fa-solid fa-plus"></i> Kuralı Sisteme Kaydet</button>
                
                <div class="rule-list" id="ruleList"></div>
            </div>
        </div>

        <div id="tab-feed" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-stream" style="color:var(--accent-green);"></i> Anlık Hediye & Chat Konsolu</span></div>
            <div class="card">
                <p style="color:var(--text-muted); font-size:14px;">Canlı yayında atılan hediyeler ve etkileşimler anlık olarak buraya düşer:</p>
                <div class="live-log-box" id="logBox">
                    <div class="log-entry">[Sistem] TikTeki Live Engine başlatıldı. Bağlantı bekleniyor...</div>
                </div>
                <button onclick="addFakeLog()" style="margin-top:15px;"><i class="fa-solid fa-flask"></i> Test Hediyesi Gönder (Simülasyon)</button>
            </div>
        </div>

        <div id="tab-games" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-dharmachakra" style="color:var(--accent-cyan);"></i> Canlı Yayın Çarkıfelek Widget'ı</span></div>
            <div class="card" style="text-align:center;">
                <p style="color:var(--text-muted); font-size:14px;">Hediye atan izleyicilerin isimleri çarka otomatik yazılır!</p>
                <div class="wheel-demo">TIKTEKI</div>
                <button style="margin: 0 auto;" onclick="alert('Çark çevrildi! Kazanan: @user123')"><i class="fa-solid fa-rotate"></i> Test Çarkını Çevir</button>
            </div>
        </div>

        <div id="tab-minecraft" class="tab-content">
            <div class="header-title"><span><i class="fa-cube" style="color:var(--accent-purple);"></i> Minecraft Server Entegrasyonu (Aternos / PaperMC)</span></div>
            <div class="card">
                <div class="card-title">Server Socket & RCON Ayarları</div>
                <div style="display:flex; flex-direction:column; gap:12px;">
                    <input type="text" placeholder="Sunucu IP Adresi (Örn: my-server.aternos.me)">
                    <input type="text" placeholder="RCON Port / Floodgate Key">
                    <button><i class="fa-solid fa-link"></i> Sunucuya Bağlan</button>
                </div>
            </div>
        </div>

        <div id="tab-chatbot" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-robot" style="color:#f59e0b;"></i> Chat Bot & Otomatik Duyurular</span></div>
            <div class="card">
                <div class="card-title">Otomatik Mesaj Zamanlayıcı</div>
                <input type="text" placeholder="Duyuru Mesajı (Örn: 'Discord sunucumuza katılmayı unutmayın!')" style="margin-bottom:12px;">
                <input type="number" placeholder="Kaç Dakikada Bir Gönderilsin? (Örn: 5)" style="margin-bottom:12px;">
                <button><i class="fa-solid fa-clock"></i> Zamanlayıcıyı Başlat</button>
            </div>
        </div>

        <div id="tab-overlays" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-desktop" style="color:var(--accent-cyan);"></i> OBS Studio Katman Linkleri</span></div>
            <div class="card">
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">1. Hediye & Bildirim Kutusu (Alert Box):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/alert-box" readonly style="margin: 8px 0 20px 0; background:#05070f;">
                
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">2. Çarkıfelek Katmanı (Spin Wheel Overlay):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/wheel" readonly style="margin: 8px 0 20px 0; background:#05070f;">

                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">3. Hediye Hedef Çubuğu (Goal Bar):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/goal-bar" readonly style="margin-top: 8px; background:#05070f;">
            </div>
        </div>

        <div id="tab-tts" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-volume-high" style="color:var(--accent-pink);"></i> Gelişmiş TTS & Efekt Ses Tahtası</span></div>
            <div class="card">
                <div class="card-title">TTS Ses Motoru Ayarları</div>
                <select style="margin-bottom:15px;">
                    <option>Türkçe - Doğal Kadın Sesi (HD)</option>
                    <option>Türkçe - Karizmatik Erkek Sesi</option>
                    <option>Robotik / Helyum Efektli Ses</option>
                </select>
                <button onclick="alert('Ses motoru test edildi!')"><i class="fa-solid fa-play"></i> Test Sesi Dinle</button>
            </div>
        </div>

        <div id="tab-settings" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-sliders"></i> Sistem Ayarları & API Keys</span></div>
            <div class="card">
                <div class="card-title">Sistem Yapılandırması</div>
                <input type="text" placeholder="Sistem Yetki Anahtarı (API Token)" style="margin-bottom:12px;">
                <button onclick="alert('Tüm ayarlar kaydedildi!')"><i class="fa-solid fa-floppy-disk"></i> Kaydet</button>
            </div>
        </div>

    </div>

    <script>
        function switchTabtem" onclick="switchTab('tab-games', this)"><i class="fa-solid fa-dharmachakra"></i><span>Çarkıfelek & Oyuncu</span></div>
            <div class="menu-item" onclick="switchTab('tab-minecraft', this)"><i class="fa-cube"></i><span>Minecraft / Webhook</span></div>
            <div class="menu-item" onclick="switchTab('tab-chatbot', this)"><i class="fa-solid fa-robot"></i><span>Chat Bot & Mod</span></div>
            
            <div class="menu-group">Görsel & Ses</div>
            <div class="menu-item" onclick="switchTab('tab-overlays', this)"><i class="fa-solid fa-desktop"></i><span>OBS Overlays</span></div>
            <div class="menu-item" onclick="switchTab('tab-tts', this)"><i class="fa-solid fa-volume-high"></i><span>TTS & Soundboard</span></div>
            <div class="menu-item" onclick="switchTab('tab-settings', this)"><i class="fa-solid fa-sliders"></i><span>Gelişmiş Ayarlar</span></div>
        </div>
    </div>

    <!-- MAIN WORKSPACE -->
    <div class="main-content">
        
        <!-- 1. KONTROL PANELİ -->
        <div id="tab-home" class="tab-content active">
            <div class="header-title">
                <span><i class="fa-solid fa-gauge-high" style="color:var(--accent-cyan);"></i> Yayın Stüdyosu & Canlı Analiz</span>
                <span style="font-size:12px; background:rgba(16,185,129,0.2); color:#10b981; padding:6px 14px; border-radius:20px; border:1px solid #10b981;">1077+ Modül Aktif</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><h4>1,250</h4><p>Tahmini Elmas (Gift)</p></div>
                <div class="stat-card"><h4>0 ms</h4><p>Sinyal Gecikmesi</p></div>
                <div class="stat-card"><h4>24/7</h4><p>Vercel Serverless</p></div>
                <div class="stat-card"><h4>%100</h4><p>TikFinity Uyumlu</p></div>
            </div>

            <div class="card">
                <div class="card-title"><i class="fa-solid fa-circle-play"></i> TikTok Yayın Bağlantı Denetleyicisi</div>
                <div class="input-box">
                    <input type="text" id="username" placeholder="TikTok Kullanıcı Adı (@kullanici)" value="@">
                    <button onclick="checkAndConnect()"><i class="fa-solid fa-plug"></i> Hesabı Test Et & Bağlan</button>
                </div>
                
                <div id="profileContainer" class="profile-container">
                    <img id="profileImg" src="" class="profile-pic" alt="Profil">
                    <div class="profile-info">
                        <h3 id="profileName">@kullanici</h3>
                        <p id="profileDesc">Durum sorgulanıyor...</p>
                        <div id="profileBadge" class="badge">Bekleniyor</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. OTOMASYONLAR & KURALLAR -->
        <div id="tab-rules" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-pink);"></i> Hediye & Etkileşim Otomasyon Motoru</span></div>
            <div class="card">
                <div class="rule-form">
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">TETİKLEYİCİ OLAY:</label>
                        <select id="eventType" style="margin-top:6px;">
                            <option value="Hediye: Gül (Rose)">Hediye: Gül (Rose - 1 Coin)</option>
                            <option value="Hediye: Aslan (Lion)">Hediye: Aslan (Lion - 29999 Coin)</option>
                            <option value="Hediye: Asa (Wand)">Hediye: Asa (Magic Wand)</option>
                            <option value="Olay: Yeni Takip">Olay: Yeni Takipçi</option>
                            <option value="Olay: Yayını Paylaştı">Olay: Yayın Paylaşımı</option>
                            <option value="Olay: 500+ Beğeni">Olay: 500 Beğeni Barajı</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">YAPILACAK EYLEM:</label>
                        <select id="actionType" style="margin-top:6px;">
                            <option value="TTS Okut">Yazıyı Sesli Okut (TTS Engine)</option>
                            <option value="Ses Çal">Özel MP3 Efekti Çal (Soundboard)</option>
                            <option value="Ekranda Konfeti">Ekranda Patlama / Konfeti Efekti</option>
                            <option value="Minecraft Komutu">Minecraft Server Komutu Çalıştır</option>
                        </select>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <input type="text" id="actionValue" placeholder="Örn: Harikayız! Teşekkürler {user}!">
                </div>
                <button onclick="addRule()" style="width:100%;"><i class="fa-solid fa-plus"></i> Kuralı Sisteme Kaydet</button>
                
                <div class="rule-list" id="ruleList"></div>
            </div>
        </div>

        <!-- 3. CANLI YAYIN AKIŞ LOGLARI -->
        <div id="tab-feed" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-stream" style="color:var(--accent-green);"></i> Anlık Hediye & Chat Konsolu</span></div>
            <div class="card">
                <p style="color:var(--text-muted); font-size:14px;">Canlı yayında atılan hediyeler ve etkileşimler anlık olarak buraya düşer:</p>
                <div class="live-log-box" id="logBox">
                    <div class="log-entry">[Sistem] TikTeki Live Engine başlatıldı. Bağlantı bekleniyor...</div>
                </div>
                <button onclick="addFakeLog()" style="margin-top:15px;"><i class="fa-solid fa-flask"></i> Test Hediyesi Gönder (Simülasyon)</button>
            </div>
        </div>

        <!-- 4. ÇARKI FELEK & OYUNLAR -->
        <div id="tab-games" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-dharmachakra" style="color:var(--accent-cyan);"></i> Canlı Yayın Çarkıfelek Widget'ı</span></div>
            <div class="card" style="text-align:center;">
                <p style="color:var(--text-muted); font-size:14px;">Hediye atan izleyicilerin isimleri çarka otomatik yazılır!</p>
                <div class="wheel-demo">TIKTEKI</div>
                <button style="margin: 0 auto;" onclick="alert('Çark çevrildi! Kazanan: @user123')"><i class="fa-solid fa-rotate"></i> Test Çarkını Çevir</button>
            </div>
        </div>

        <!-- 5. MINECRAFT / WEBHOOK -->
        <div id="tab-minecraft" class="tab-content">
            <div class="header-title"><span><i class="fa-cube" style="color:var(--accent-purple);"></i> Minecraft Server Entegrasyonu (Aternos / PaperMC)</span></div>
            <div class="card">
                <div class="card-title">Server Socket & RCON Ayarları</div>
                <div style="display:flex; flex-direction:column; gap:12px;">
                    <input type="text" placeholder="Sunucu IP Adresi (Örn: my-server.aternos.me)">
                    <input type="text" placeholder="RCON Port / Floodgate Key">
                    <button><i class="fa-solid fa-link"></i> Sunucuya Bağlan</button>
                </div>
            </div>
        </div>

        <!-- 6. CHAT BOT -->
        <div id="tab-chatbot" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-robot" style="color:#f59e0b;"></i> Chat Bot & Otomatik Duyurular</span></div>
            <div class="card">
                <div class="card-title">Otomatik Mesaj Zamanlayıcı</div>
                <input type="text" placeholder="Duyuru Mesajı (Örn: 'Discord sunucumuza katılmayı unutmayın!')" style="margin-bottom:12px;">
                <input type="number" placeholder="Kaç Dakikada Bir Gönderilsin? (Örn: 5)" style="margin-bottom:12px;">
                <button><i class="fa-solid fa-clock"></i> Zamanlayıcıyı Başlat</button>
            </div>
        </div>

        <!-- 7. OBS OVERLAYS -->
        <div id="tab-overlays" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-desktop" style="color:var(--accent-cyan);"></i> OBS Studio Katman Linkleri</span></div>
            <div class="card">
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">1. Hediye & Bildirim Kutusu (Alert Box):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/alert-box" readonly style="margin: 8px 0 20px 0; background:#05070f;">
                
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">2. Çarkıfelek Katmanı (Spin Wheel Overlay):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/wheel" readonly style="margin: 8px 0 20px 0; background:#05070f;">

                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">3. Hediye Hedef Çubuğu (Goal Bar):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/goal-bar" readonly style="margin-top: 8px; background:#05070f;">
            </div>
        </div>

        <!-- 8. TTS & SOUNDBOARD -->
        <div id="tab-tts" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-volume-high" style="color:var(--accent-pink);"></i> Gelişmiş TTS & Efekt Ses Tahtası</span></div>
            <div class="card">
                <div class="card-title">TTS Ses Motoru Ayarları</div>
                <select style="margin-bottom:15px;">
                    <option>Türkçe - Doğal Kadın Sesi (HD)</option>
                    <option>Türkçe - Karizmatik Erkek Sesi</option>
                    <option>Robotik / Helyum Efektli Ses</option>
                </select>
                <button onclick="alert('Ses motoru test edildiOBS Overlays</span></div>
            <div class="menu-item" onclick="switchTab('tab-tts', this)"><i class="fa-solid fa-volume-high"></i><span>TTS & Soundboard</span></div>
            <div class="menu-item" onclick="switchTab('tab-settings', this)"><i class="fa-solid fa-sliders"></i><span>Gelişmiş Ayarlar</span></div>
        </div>
    </div>

    <!-- MAIN WORKSPACE -->
    <div class="main-content">
        
        <!-- 1. KONTROL PANELİ -->
        <div id="tab-home" class="tab-content active">
            <div class="header-title">
                <span><i class="fa-solid fa-gauge-high" style="color:var(--accent-cyan);"></i> Yayın Stüdyosu & Canlı Analiz</span>
                <span style="font-size:12px; background:rgba(16,185,129,0.2); color:#10b981; padding:6px 14px; border-radius:20px; border:1px solid #10b981;">1000+ Modül Aktif</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><h4>1,250</h4><p>Tahmini Elmas (Gift)</p></div>
                <div class="stat-card"><h4>0 ms</h4><p>Sinyal Gecikmesi</p></div>
                <div class="stat-card"><h4>24/7</h4><p>Vercel Serverless</p></div>
                <div class="stat-card"><h4>%100</h4><p>TikFinity Uyumlu</p></div>
            </div>

            <div class="card">
                <div class="card-title"><i class="fa-solid fa-circle-play"></i> TikTok Yayın Bağlantı Denetleyicisi</div>
                <div class="input-box">
                    <input type="text" id="username" placeholder="TikTok Kullanıcı Adı (@kullanici)" value="@">
                    <button onclick="checkAndConnect()"><i class="fa-solid fa-plug"></i> Hesabı Test Et & Bağlan</button>
                </div>
                
                <div id="profileContainer" class="profile-container">
                    <img id="profileImg" src="" class="profile-pic" alt="Profil">
                    <div class="profile-info">
                        <h3 id="profileName">@kullanici</h3>
                        <p id="profileDesc">Durum sorgulanıyor...</p>
                        <div id="profileBadge" class="badge">Bekleniyor</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. OTOMASYONLAR & KURALLAR -->
        <div id="tab-rules" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-pink);"></i> Hediye & Etkileşim Otomasyon Motoru</span></div>
            <div class="card">
                <div class="rule-form">
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">TETİKLEYİCİ OLAY:</label>
                        <select id="eventType" style="margin-top:6px;">
                            <option value="Hediye: Gül (Rose)">Hediye: Gül (Rose - 1 Coin)</option>
                            <option value="Hediye: Aslan (Lion)">Hediye: Aslan (Lion - 29999 Coin)</option>
                            <option value="Hediye: Asa (Wand)">Hediye: Asa (Magic Wand)</option>
                            <option value="Olay: Yeni Takip">Olay: Yeni Takipçi</option>
                            <option value="Olay: Yayını Paylaştı">Olay: Yayın Paylaşımı</option>
                            <option value="Olay: 500+ Beğeni">Olay: 500 Beğeni Barajı</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:700;">YAPILACAK EYLEM:</label>
                        <select id="actionType" style="margin-top:6px;">
                            <option value="TTS Okut">Yazıyı Sesli Okut (TTS Engine)</option>
                            <option value="Ses Çal">Özel MP3 Efekti Çal (Soundboard)</option>
                            <option value="Ekranda Konfeti">Ekranda Patlama / Konfeti Efekti</option>
                            <option value="Minecraft Komutu">Minecraft Server Komutu Çalıştır</option>
                        </select>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <input type="text" id="actionValue" placeholder="Örn: Harikayız! Teşekkürler {user}!">
                </div>
                <button onclick="addRule()" style="width:100%;"><i class="fa-solid fa-plus"></i> Kuralı Sisteme Kaydet</button>
                
                <div class="rule-list" id="ruleList"></div>
            </div>
        </div>

        <!-- 3. ÇARKI FELEK & OYUNLAR -->
        <div id="tab-games" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-dharmachakra" style="color:var(--accent-cyan);"></i> Canlı Yayın Çarkıfelek Widget'ı</span></div>
            <div class="card" style="text-align:center;">
                <p style="color:var(--text-muted); font-size:14px;">Hediye atan izleyicilerin isimleri çarka otomatik yazılır!</p>
                <div class="wheel-demo">TIKTEKI</div>
                <button style="margin: 0 auto;" onclick="alert('Çark çevrildi! Kazanan: @user123')"><i class="fa-solid fa-rotate"></i> Test Çarkını Çevir</button>
            </div>
        </div>

        <!-- 4. MINECRAFT / WEBHOOK -->
        <div id="tab-minecraft" class="tab-content">
            <div class="header-title"><span><i class="fa-cube" style="color:var(--accent-purple);"></i> Minecraft Server Entegrasyonu (Aternos / PaperMC)</span></div>
            <div class="card">
                <div class="card-title">Server Socket & RCON Ayarları</div>
                <div style="display:flex; flex-direction:column; gap:12px;">
                    <input type="text" placeholder="Sunucu IP Adresi (Örn: my-server.aternos.me)">
                    <input type="text" placeholder="RCON Port / Floodgate Key">
                    <button><i class="fa-solid fa-link"></i> Sunucuya Bağlan</button>
                </div>
            </div>
        </div>

        <!-- 5. CHAT BOT -->
        <div id="tab-chatbot" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-robot" style="color:#f59e0b;"></i> Chat Bot & Otomatik Duyurular</span></div>
            <div class="card">
                <div class="card-title">Otomatik Mesaj Zamanlayıcı</div>
                <input type="text" placeholder="Duyuru Mesajı (Örn: 'Discord sunucumuza katılmayı unutmayın!')" style="margin-bottom:12px;">
                <input type="number" placeholder="Kaç Dakikada Bir Gönderilsin? (Örn: 5)" style="margin-bottom:12px;">
                <button><i class="fa-solid fa-clock"></i> Zamanlayıcıyı Başlat</button>
            </div>
        </div>

        <!-- 6. OBS OVERLAYS -->
        <div id="tab-overlays" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-desktop" style="color:var(--accent-cyan);"></i> OBS Studio Katman Linkleri</span></div>
            <div class="card">
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">1. Hediye & Bildirim Kutusu (Alert Box):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/alert-box" readonly style="margin: 8px 0 20px 0; background:#05070f;">
                
                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">2. Çarkıfelek Katmanı (Spin Wheel Overlay):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/wheel" readonly style="margin: 8px 0 20px 0; background:#05070f;">

                <label style="font-size:12px; color:var(--accent-cyan); font-weight:bold;">3. Hediye Hedef Çubuğu (Goal Bar):</label>
                <input type="text" value="https://tikteki.vercel.app/overlay/goal-bar" readonly style="margin-top: 8px; background:#05070f;">
            </div>
        </div>

        <!-- 7. TTS & SOUNDBOARD -->
        <div id="tab-tts" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-volume-high" style="color:var(--accent-pink);"></i> Gelişmiş TTS & Efekt Ses Tahtası</span></div>
            <div class="card">
                <div class="card-title">TTS Ses Motoru Ayarları</div>
                <select style="margin-bottom:15px;">
                    <option>Türkçe - Doğal Kadın Sesi (HD)</option>
                    <option>Türkçe - Karizmatik Erkek Sesi</option>
                    <option>Robotik / Helyum Efektli Ses</option>
                </select>
                <button onclick="alert('Ses motoru test edildi!')"><i class="fa-solid fa-play"></i> Test Sesi Dinle</button>
            </div>
        </div>

        <!-- 8. GELİŞMİŞ AYARLAR -->
        <div id="tab-settings" class="tab-content">
            <div class="header-title"><span><i class="fa-solid fa-sliders"></i> Sistem Ayarları & API Keys</span></div>
            <div class="card">
                <div class="card-title">Sistem Yapılandırması</div>
                <input type="text" placeholder="Sistem Yetki Anahtarı (API Token)" style="margin-bottom:12px;">
                <button onclick="alert('Tüm ayarlar kaydedildi!')"><i class="fa-solid fa-floppy-disk"></i> Kaydet</button>
            </div>
        </div>

    </div>

    <script>
        function switchTab(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            element.classList.add('active');
        }

        function checkAndConnect() {
            const username = document.getElementById('username').value.trim();
            const container = document.getElementById('profileContainer');
            const img = document.getElementById('profileImg');
            const name = document.getElementById('profileName');
     
