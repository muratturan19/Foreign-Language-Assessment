# Render Deployment Guide

Bu rehber, Foreign Language Assessment uygulamasının Render platformunda nasıl deploy edileceğini adım adım açıklar.

## Gereksinimler

- Render.com hesabı (ücretsiz veya ücretli plan)
- GitHub/GitLab/Bitbucket repository erişimi
- Email servisi (SMTP veya SendGrid)
- OpenAI API key (GPT-4/GPT-5 için)

## Özellikler

Bu deployment konfigürasyonu aşağıdaki özellikleri destekler:

✅ **Ses Dosyası İşleme**: FFmpeg ile otomatik audio format dönüşümü
✅ **Email Gönderimi**: SMTP veya SendGrid ile rapor gönderme
✅ **Persistent Storage**: Audio ve report dosyaları için kalıcı disk
✅ **Auto-Deploy**: Main branch'e push yapıldığında otomatik deployment
✅ **Health Check**: Otomatik sağlık kontrolü
✅ **Static File Serving**: React frontend'i FastAPI ile serve etme

## Deployment Adımları

### 1. Repository'yi Hazırlama

GitHub/GitLab/Bitbucket'ta repository'nizin hazır olduğundan emin olun.

### 2. Render'da Yeni Web Service Oluşturma

1. [Render Dashboard](https://dashboard.render.com/) adresine gidin
2. "New +" butonuna tıklayın ve "Web Service" seçin
3. Repository'nizi bağlayın (GitHub/GitLab/Bitbucket)
4. Bu repository'yi seçin: `Foreign-Language-Assessment`

### 3. Deployment Yöntemi

İki farklı yöntemle deploy edebilirsiniz:

#### Yöntem A: render.yaml ile Otomatik Deployment (Önerilen)

Render otomatik olarak `render.yaml` dosyasını tespit edecek ve gerekli ayarları yapacaktır.

1. "You are deploying a Blueprint" mesajını göreceksiniz
2. Service name'i kontrol edin: `foreign-language-assessment`
3. "Apply" butonuna tıklayın

#### Yöntem B: Manuel Konfigürasyon

Eğer render.yaml kullanmak istemezseniz, manuel olarak yapılandırabilirsiniz:

**Build & Deploy Settings:**
- **Environment**: Python
- **Region**: Frankfurt (veya size yakın bir bölge)
- **Branch**: main (veya deploy etmek istediğiniz branch)
- **Build Command**:
  ```bash
  apt-get update && apt-get install -y ffmpeg && pip install -r backend/requirements.txt && npm install --prefix frontend
  ```
- **Start Command**:
  ```bash
  bash start.sh
  ```

### 4. Environment Variables Ayarlama

Render Dashboard'da Environment sekmesine gidin ve aşağıdaki değişkenleri ekleyin:

#### Zorunlu Değişkenler

| Variable | Açıklama | Örnek Değer |
|----------|----------|-------------|
| `APP_SECRET_TOKEN` | API kimlik doğrulama token'ı | Render'ın "Generate Value" özelliğini kullanın |
| `APP_BASE_URL` | Uygulamanızın URL'i | `https://foreign-language-assessment.onrender.com` |
| `TARGET_EMAIL` | Varsayılan rapor alıcı email'i | `your-email@example.com` |

#### Email Konfigürasyonu (Seçeneklerden birini seçin)

**Seçenek 1: SMTP (Gmail, Outlook, vb.)**

| Variable | Açıklama | Örnek Değer |
|----------|----------|-------------|
| `EMAIL_PROVIDER` | Email servisi tipi | `smtp` |
| `SMTP_HOST` | SMTP sunucu adresi | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port numarası | `587` (TLS) veya `465` (SSL) |
| `SMTP_USERNAME` | SMTP kullanıcı adı | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP şifresi veya app password | `your-app-password` |
| `EMAIL_DEFAULT_SENDER` | Gönderen email adresi | `noreply@yourdomain.com` |

**Gmail için App Password Oluşturma:**
1. Google Account Settings → Security
2. 2-Step Verification'ı aktifleştirin
3. App Passwords bölümüne gidin
4. "Mail" için yeni bir app password oluşturun

**Seçenek 2: SendGrid (Önerilen - Üretim için)**

| Variable | Açıklama | Örnek Değer |
|----------|----------|-------------|
| `EMAIL_PROVIDER` | Email servisi tipi | `sendgrid` |
| `SENDGRID_API_KEY` | SendGrid API anahtarı | `SG.xxxxxxxxxxxxxxxxxxxxxxxx` |
| `EMAIL_DEFAULT_SENDER` | Gönderen email adresi | `noreply@yourdomain.com` |

#### GPT API Konfigürasyonu (LLM Evaluation için)

| Variable | Açıklama | Örnek Değer |
|----------|----------|-------------|
| `GPT5_API_KEY` | OpenAI API anahtarı | `sk-proj-xxxxxxxxxxxxxxxx` |
| `GPT5_API_BASE_URL` | API endpoint (opsiyonel) | `https://api.openai.com/v1` |
| `GPT5_MODEL` | Kullanılacak model | `gpt-4` veya `gpt-4-turbo` |
| `GPT5_TEMPERATURE` | Model temperature (opsiyonel) | `0.3` |

#### Opsiyonel Değişkenler

| Variable | Açıklama | Varsayılan Değer |
|----------|----------|------------------|
| `REPORT_LANGUAGE` | Rapor dili | `en` |
| `STORE_TRANSCRIPTS` | Transcript'leri kaydet | `true` |

#### Frontend Build Variables

Frontend build sırasında kullanılır:

| Variable | Açıklama | Örnek Değer |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | Backend API URL'i | `https://foreign-language-assessment.onrender.com` |
| `VITE_APP_SECRET_TOKEN` | Frontend'in kullanacağı token | `APP_SECRET_TOKEN` ile aynı değer |

### 5. Disk Storage Ayarlama

Ses dosyaları ve raporları saklamak için persistent disk gereklidir:

1. Render Dashboard'da service'inize gidin
2. "Disks" sekmesine tıklayın
3. "Add Disk" butonuna tıklayın
4. Aşağıdaki bilgileri girin:
   - **Name**: `assessment-data`
   - **Mount Path**: `/opt/render/project/src/backend`
   - **Size**: `1 GB` (başlangıç için yeterli, gerekirse artırabilirsiniz)

**Not**: Eğer render.yaml kullandıysanız, disk otomatik olarak oluşturulacaktır.

### 6. Deployment'ı Başlatma

1. Tüm environment variables'ları ekledikten sonra
2. "Manual Deploy" → "Deploy latest commit" ile deployment'ı başlatın
3. Logs sekmesinden build ve deployment sürecini takip edin

Build süreci yaklaşık 5-10 dakika sürebilir (FFmpeg kurulumu + frontend build).

## Deployment Sonrası Kontroller

### 1. Health Check

Uygulamanızın çalıştığını kontrol edin:

```bash
curl https://your-app.onrender.com/health
```

Beklenen yanıt:
```json
{
  "status": "ok",
  "timestamp": "2025-11-14T12:00:00.000000"
}
```

### 2. Email Konfigürasyonunu Test Etme

```bash
curl -X GET https://your-app.onrender.com/api/config/email \
  -H "Authorization: Bearer YOUR_SECRET_TOKEN"
```

Beklenen yanıt:
```json
{
  "configured": true,
  "provider": "smtp",
  "settings": {
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "your-email@gmail.com",
    "from_email": "noreply@yourdomain.com"
  }
}
```

### 3. GPT-5 Konfigürasyonunu Test Etme

```bash
curl -X GET https://your-app.onrender.com/api/config/gpt5 \
  -H "Authorization: Bearer YOUR_SECRET_TOKEN"
```

Beklenen yanıt:
```json
{
  "configured": true
}
```

### 4. Frontend'i Test Etme

Tarayıcınızda şu adresi açın:
```
https://your-app.onrender.com
```

React uygulaması yüklenmelidir.

## Önemli Notlar

### Free Plan Sınırlamaları

Render'ın ücretsiz planında:
- ❌ İlk request'ten sonra uygulama uyur (15 dakika inaktivite sonrası)
- ❌ Aylık 750 saat sınırı var
- ❌ Persistent disk yok (dosyalar kaybolabilir)
- ✅ Test ve geliştirme için uygundur

### Starter Plan Avantajları

- ✅ Uygulama hiç uyumaz
- ✅ Persistent disk desteği
- ✅ Daha fazla CPU ve RAM
- ✅ Üretim ortamı için önerilir

### Persistent Disk Önemli!

Eğer persistent disk eklemezseniz:
- Ses dosyaları her deployment'ta silinir
- Raporlar kaybolur
- Token'lar geçersiz olur

**Üretim ortamı için persistent disk zorunludur.**

### FFmpeg Gereksinimleri

Ses dosyası işleme (audio transcoding) için FFmpeg gereklidir:
- render.yaml'daki build command otomatik olarak FFmpeg'i kurar
- Manuel deployment'ta build command'e FFmpeg kurulumunu eklemeyi unutmayın

## Sorun Giderme

### Build Hatası: "FFmpeg not found"

**Çözüm**: Build command'e FFmpeg kurulumunu ekleyin:
```bash
apt-get update && apt-get install -y ffmpeg
```

### Hata: "Failed to send email"

**Olası sebepler**:
1. Email environment variables yanlış ayarlanmış
2. SMTP şifresi yanlış (Gmail için app password kullanın)
3. SendGrid API key geçersiz

**Kontrol**:
```bash
curl -X GET https://your-app.onrender.com/api/config/email \
  -H "Authorization: Bearer YOUR_SECRET_TOKEN"
```

### Hata: "Audio file not found"

**Sebep**: Persistent disk ayarlanmamış veya mount path yanlış

**Çözüm**:
1. Render Dashboard → Disks → Add Disk
2. Mount path'i `/opt/render/project/src/backend` olarak ayarlayın

### Frontend'e Erişilemiyor

**Olası sebepler**:
1. Frontend build edilmemiş
2. StaticFiles mount yanlış

**Kontrol**: Logs'ta şunu görmelisiniz:
```
npm run build --prefix frontend
✓ built in 15.23s
```

### CORS Hatası

**Çözüm**: `VITE_API_BASE_URL` environment variable'ını doğru ayarlayın:
```bash
VITE_API_BASE_URL=https://your-app.onrender.com
```

## Güncelleme ve Yeniden Deployment

### Otomatik Deployment

render.yaml'da `autoDeploy: true` ayarlandığı için:
- Main branch'e her push'ta otomatik deploy edilir
- Manual deployment'a gerek yoktur

### Manuel Deployment

1. Render Dashboard'da service'inize gidin
2. "Manual Deploy" → "Deploy latest commit"
3. Logs'tan süreci takip edin

## Güvenlik Önerileri

1. **Environment Variables**: Hassas bilgileri (API keys, passwords) asla kod içinde saklamayın
2. **APP_SECRET_TOKEN**: Güçlü bir token kullanın (Render'ın "Generate Value" özelliğini kullanın)
3. **SMTP Passwords**: Gmail için mutlaka App Password kullanın
4. **HTTPS**: Render otomatik olarak HTTPS sağlar, HTTP endpoint'leri kapatın
5. **Email Domain**: Üretim ortamında kendi domain'inizden email gönderin (SPF/DKIM ayarları)

## Performans Optimizasyonu

### Üretim Ortamı İçin Öneriler

1. **Starter Plan veya Üzeri**: Free plan üretim için uygun değildir
2. **Region Seçimi**: Kullanıcılarınıza en yakın bölgeyi seçin
3. **Disk Boyutu**: Kullanım durumunuza göre disk boyutunu artırın
4. **Caching**: GPT-5 client'ında caching aktif (otomatik)
5. **CDN**: Static assets için CDN kullanmayı düşünün

## Maliyet Tahmini

### Free Plan
- Maliyet: $0/ay
- Sınırlamalar: 750 saat/ay, disk yok, sleep mode
- Kullanım: Test ve demo

### Starter Plan
- Maliyet: ~$7/ay (web service)
- Disk: $0.25/GB/ay
- Toplam: ~$7.25/ay (1GB disk ile)
- Kullanım: Küçük üretim ortamları

### Pro Plan
- Maliyet: ~$25/ay
- Daha fazla CPU/RAM
- Kullanım: Yüksek trafikli uygulamalar

## Ek Kaynaklar

- [Render Documentation](https://render.com/docs)
- [Render Dashboard](https://dashboard.render.com/)
- [Render Status Page](https://status.render.com/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

## Destek

Sorunlarla karşılaşırsanız:

1. Önce Render logs'unu kontrol edin
2. Environment variables'ları doğrulayın
3. Health check endpoint'ini test edin
4. Bu repository'nin Issues sekmesinde soru sorabilirsiniz

---

**Son Güncelleme**: 2025-11-14
**Desteklenen Render API Versiyonu**: v1
**Test Edilmiş Node Version**: 18.x
**Test Edilmiş Python Version**: 3.11
