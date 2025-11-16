# Render Deployment Kurulum Rehberi

Bu proje FFmpeg gerektirdiği için Render'da özel build yapılandırması gerekir.

## Adım 1: Render Dashboard'da Web Service Oluşturun

1. Render Dashboard'a gidin: https://dashboard.render.com/
2. "New +" butonuna tıklayın ve "Web Service" seçin
3. GitHub repository'nizi bağlayın

## Adım 2: Build & Deploy Ayarları

### Environment (Ortam)
- **Runtime**: `Python 3`

### Build Command (Build Komutu)
```bash
bash build.sh
```

### Start Command (Başlatma Komutu)
```bash
bash start.sh
```

### Root Directory (Kök Dizin)
- Boş bırakın (proje kökünde çalışacak)

## Adım 3: Environment Variables (Ortam Değişkenleri)

Aşağıdaki environment variable'ları ekleyin:

### Gerekli Değişkenler:
```
APP_SECRET_TOKEN=<güvenli-bir-token-oluşturun>
OPENAI_API_KEY=<openai-api-key>
EMAIL_API_KEY=<email-api-key>
```

### Opsiyonel Değişkenler:
```
REPORT_LANGUAGE=en
STORE_TRANSCRIPTS=true
```

### Otomatik Değişkenler:
- `RENDER_EXTERNAL_URL` - Render tarafından otomatik olarak sağlanır
- `PORT` - Render tarafından otomatik olarak sağlanır

## Adım 4: Advanced Ayarları (Opsiyonel)

### Health Check Path:
```
/health
```

### Auto-Deploy:
- "Auto-Deploy" seçeneğini aktif edin (main branch'e push olduğunda otomatik deploy olur)

## Adım 5: Persistent Disk (Opsiyonel)

Eğer audio dosyalarını ve raporları kalıcı olarak saklamak istiyorsanız:

1. "Disks" sekmesine gidin
2. "Add Disk" butonuna tıklayın
3. Ayarlar:
   - **Name**: `assessment-data`
   - **Mount Path**: `/opt/render/project/src/backend`
   - **Size**: `1 GB` (ihtiyacınıza göre ayarlayın)

## FFmpeg Kurulumu Hakkında

`build.sh` scripti otomatik olarak şunları yapar:
1. ✅ FFmpeg'i sistem paketinden kurar (`apt-get install ffmpeg`)
2. ✅ Python bağımlılıklarını yükler
3. ✅ Frontend'i build eder

## Deployment Sonrası Kontrol

Deploy tamamlandıktan sonra:

1. Logs'u kontrol edin ve FFmpeg kurulumunun başarılı olduğunu doğrulayın
2. Health check endpoint'ini test edin: `https://your-app.onrender.com/health`
3. Ses kaydı özelliğini test edin

## Sorun Giderme

### FFmpeg bulunamıyor hatası:
- Build logs'unda FFmpeg kurulumunun başarılı olduğunu kontrol edin
- Build command'in `bash build.sh` olduğundan emin olun

### Frontend build hatası:
- `RENDER_EXTERNAL_URL` environment variable'ının otomatik olarak set edildiğinden emin olun

### Audio conversion hatası:
- Logs'da FFmpeg'in PATH'de olduğunu kontrol edin
- Ses dosyası formatının desteklendiğinden emin olun (webm, ogg, wav, m4a → mp3)

## İletişim

Sorunlarınız için GitHub Issues kullanabilirsiniz.
