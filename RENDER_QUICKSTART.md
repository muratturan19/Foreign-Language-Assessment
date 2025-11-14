# Render Hızlı Başlangıç Kılavuzu

Bu uygulamayı Render'da 10 dakikada deploy edin!

## 🚀 Hızlı Adımlar

### 1. Repository'yi Render'a Bağlayın

1. [dashboard.render.com](https://dashboard.render.com) adresine gidin
2. "New +" → "Web Service"
3. Repository'nizi bağlayın ve seçin
4. "Apply" (render.yaml otomatik algılanacak)

### 2. Environment Variables Ekleyin

Render Dashboard → Environment sekmesinde şu değişkenleri ekleyin:

#### Minimum Gereksinimler (Test için)

```bash
APP_SECRET_TOKEN=<Generate Value butonunu kullanın>
APP_BASE_URL=https://your-app-name.onrender.com
TARGET_EMAIL=your-email@example.com
```

#### Email (Gmail Örneği)

```bash
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=<Gmail App Password>
EMAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

**Gmail App Password**: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

#### GPT API (Opsiyonel - LLM Evaluation için)

```bash
GPT5_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
GPT5_MODEL=gpt-4
```

#### Frontend Variables

```bash
VITE_API_BASE_URL=https://your-app-name.onrender.com
VITE_APP_SECRET_TOKEN=<APP_SECRET_TOKEN ile aynı değer>
```

### 3. Disk Ekleyin (Önemli!)

Render Dashboard → Disks → Add Disk:

- **Name**: `assessment-data`
- **Mount Path**: `/opt/render/project/src/backend`
- **Size**: `1 GB`

### 4. Deploy Edin

"Manual Deploy" → "Deploy latest commit"

Build ~5-10 dakika sürer (FFmpeg + Frontend build)

## ✅ Test

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Email config
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-app-name.onrender.com/api/config/email
```

## 🎯 Önemli Notlar

- **Free Plan**: Uygulama 15 dakika inaktiviteden sonra uyur, persistent disk yoktur
- **Starter Plan ($7/ay)**: Üretim için önerilir, disk desteği vardır
- **FFmpeg**: Otomatik kurulur (ses dosyası işleme için gerekli)
- **Auto-Deploy**: Main branch'e push yapınca otomatik deploy olur

## 📚 Detaylı Rehber

Tüm detaylar için: [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)

## ⚡ Sorun Giderme Hızlı Çözümler

| Sorun | Çözüm |
|-------|-------|
| "FFmpeg not found" | Build command'de FFmpeg kurulumu var mı kontrol edin |
| Email gönderilmiyor | Gmail için App Password kullanın |
| Audio dosyası yok | Persistent disk ekleyin |
| Frontend yüklenmiyor | VITE_API_BASE_URL doğru mu kontrol edin |

## 🌟 Üretim İçin Checklist

- [ ] Starter plan veya üzeri
- [ ] Persistent disk eklendi
- [ ] Email ayarları test edildi
- [ ] GPT API key eklendi
- [ ] APP_SECRET_TOKEN güçlü bir değer
- [ ] APP_BASE_URL doğru domain
- [ ] Health check çalışıyor

---

Kolay gelsin! 🎉
