# Render.com'a Deployment Kılavuzu

Bu proje FFmpeg gerektirdiği için Docker container kullanarak Render'da deploy edilmelidir.

## Otomatik Deployment (Blueprint - Önerilen)

### 1. Render Blueprint ile Deploy

1. Render Dashboard'a gidin: https://dashboard.render.com/
2. **New +** butonuna tıklayın
3. **Blueprint** seçeneğini seçin
4. GitHub repository'nizi bağlayın
5. Repository seçin: `Foreign-Language-Assessment`
6. Branch seçin: `main`
7. Render otomatik olarak `render.yaml` dosyasını algılayacak ve ayarları uygulayacaktır

### 2. Environment Variables Ekleyin

Blueprint deployment'tan sonra, servis ayarlarına gidip şu environment variable'ları ekleyin:

- `OPENAI_API_KEY`: OpenAI API anahtarınız (opsiyonel, GPT özelliği için)
- `EMAIL_*`: Email göndermek için SMTP ayarları (opsiyonel)

Diğer environment variable'lar (`APP_SECRET_TOKEN`, `REPORT_LANGUAGE`, `STORE_TRANSCRIPTS`) `render.yaml` tarafından otomatik ayarlanır.

---

## Manuel Deployment

Eğer Blueprint çalışmazsa, manuel olarak aşağıdaki adımları izleyin:

### 1. Yeni Web Service Oluşturun

1. Render Dashboard: https://dashboard.render.com/
2. **New +** → **Web Service**
3. GitHub repository'nizi bağlayın
4. Repository seçin: `Foreign-Language-Assessment`

### 2. Temel Ayarlar

| Ayar | Değer |
|------|-------|
| **Name** | `foreign-language-assessment` |
| **Region** | `Frankfurt` (veya size yakın bölge) |
| **Branch** | `main` |
| **Runtime** | `Docker` ⚠️ **Önemli: Python değil, Docker seçin!** |

### 3. Environment Variables

Settings → Environment → Add Environment Variable:

| Key | Value |
|-----|-------|
| `APP_SECRET_TOKEN` | (güçlü bir random token, örn: 32 karakter) |
| `REPORT_LANGUAGE` | `en` |
| `STORE_TRANSCRIPTS` | `true` |
| `OPENAI_API_KEY` | (OpenAI anahtarınız - opsiyonel) |

### 4. Persistent Disk (Opsiyonel)

Ses dosyalarını ve raporları kalıcı olarak saklamak için:

1. Settings → Disks → Add Disk
2. **Name**: `assessment-data`
3. **Mount Path**: `/app/backend`
4. **Size**: `1 GB`

### 5. Health Check (Opsiyonel)

Settings → Health & Alerts:
- **Health Check Path**: `/health`

### 6. Deploy

**Create Web Service** veya **Manual Deploy** butonuna tıklayın.

---

## Deployment Sonrası

### Build Logs'u Kontrol Edin

Deployment sırasında şunları göreceksiniz:

```
==> Building Docker image...
==> Installing FFmpeg...
==> Installing Python dependencies...
==> Installing Node.js dependencies...
==> Building frontend...
==> Deploy successful!
```

### Test Edin

Deploy tamamlandıktan sonra:

1. Render'ın verdiği URL'yi açın (örn: `https://foreign-language-assessment.onrender.com`)
2. Ana sayfa yüklenmelidir
3. `/health` endpoint'ini test edin
4. Bir değerlendirme oluşturmayı deneyin

---

## Sorun Giderme

### FFmpeg Bulunamıyor Hatası

**Hata:**
```
exec: ffmpeg: not found
```

**Çözüm:**
- Runtime'ın **Docker** olduğundan emin olun (Python değil!)
- `Dockerfile` dosyasının repository'de mevcut olduğundan emin olun

### uvicorn Bulunamıyor Hatası

**Hata:**
```
exec: uvicorn: not found
```

**Çözüm:**
- Runtime'ın **Docker** olduğundan emin olun
- `backend/requirements.txt` dosyasında `uvicorn` olduğundan emin olun

### Frontend Build Hatası

**Hata:**
```
npm ERR! code ELIFECYCLE
```

**Çözüm:**
- `frontend/package.json` dosyasını kontrol edin
- Build script'inin doğru olduğundan emin olun: `"build": "vite build"`

### Disk Mount Sorunları

Eğer disk mount çalışmıyorsa:
1. Mount path'in `/app/backend` olduğundan emin olun
2. Dockerfile'da directory'nin oluşturulduğundan emin olun (`mkdir -p backend/audio_files backend/reports`)

---

## Önemli Notlar

1. **FFmpeg**: Docker image içinde otomatik kurulur
2. **Frontend**: Build sırasında otomatik oluşturulur
3. **Port**: Render otomatik `$PORT` environment variable'ı sağlar
4. **HTTPS**: Render otomatik HTTPS sertifikası sağlar
5. **Free Plan**: İlk deploy 10-15 dakika sürebilir, sonraki deploylar daha hızlıdır

---

## Yardım

Sorun yaşarsanız:
- Render deployment logs'unu kontrol edin
- GitHub Issues açın: https://github.com/muratturan19/Foreign-Language-Assessment/issues
