# Foreign Language Assessment Platform

Bu depo, TOEFL / iTEP / IELTS rubriklerini temel alan bir İngilizce konuşma değerlendirme koçunu uçtan uca sunar. Uygulama artık yalnızca bir fikir dokümanı değil; FastAPI tabanlı backend, React + Vite frontend, raporlama katmanı, ses yükleme ve e-posta paylaşımıyla çalışan bir prototip içerir. Ayrıntılı gereksinimler için [docs/SPEC.md](docs/SPEC.md) ve mimari notlar için [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) dosyalarına bakabilirsiniz.

## Mimari Özet

- **Backend (FastAPI)**
  - Oturum ve sohbet akışını yönetir, katılımcı onayını takip eder ve konuşma kayıtlarını saklar. (`backend/app/main.py`)
  - Heuristik bir değerlendirme motoru, JSON tabanlı rubrik dosyalarını okuyarak TOEFL/iTEP/IELTS çıktıları üretir ve varsa GPT-5 API cevabıyla sonuçları birleştirir. (`backend/app/services/evaluation.py`)
  - HTML raporu kalıcı olarak kaydeder, son raporu dosya sistemi üzerinden indirilebilir hale getirir ve e-posta gönderirken rapor + ses kaydını ek olarak iliştirir.
- **Frontend (React + Vite)**
  - Türkçe bir yönetim arayüzü üzerinden katılımcı bilgisi toplar, oturum başlatır ve interviewer rolünde otomatik konuşma akışını gösterir. (`frontend/src/components/ChatPanel.tsx`)
  - Mikrofon izni alıp tarayıcıda kayıt yapar, görüşme sonunda backend'e base64 kodlu ses yükler ve değerlendirme çıktılarını kartlar halinde render eder.
  - SMTP/GPT5 yapılandırmasını UI üzerinden güncelleme, rapor paylaşma ve e-posta gönderimini tetikleme bileşenleri içerir.

## Öne Çıkan Özellikler

- 🧭 **Çoklu standart değerlendirme** – TOEFL (0–4), iTEP (0–6) ve IELTS (0–9) kriterleri için skor, yorum, CEFR eşlemesi, yaygın hatalar ve aksiyon planları üretir. Gerektiğinde GPT-5 değerlendirmeleriyle otomatik birleştirilir.
- 🧠 **CEFR uyumlu öneriler** – Transkript metriklerine göre common error tespiti, kanıt cümleleri ve CEFR seviyesine göre 5 maddelik aksiyon planı döndürür.
- 🗂️ **JSON ile konfigüre edilebilir rubrikler** – Yeni standart eklemek `configs/<standard>/<version>.json` dosyası oluşturmakla sınırlıdır; uygulama kriterleri ve ağırlıkları bu dosyalardan okur.
- 📨 **Raporlama ve e-posta** – HTML raporu disk üzerinde saklar, paylaşılabilir token üretir ve e-posta gönderiminde son rapor ile varsa ses kaydını otomatik ekler.
- 🎙️ **Ses kaydı ve yükleme** – Frontend tarayıcı API'lerini kullanarak MP3/WebM kaydı alır, backend bu kaydı disk üzerinde saklar ve e-posta ekine dönüştürür.
- 🔐 **Token tabanlı güvenlik** – Backend ve frontend aynı `APP_SECRET_TOKEN` değerini kullanır; tüm API çağrıları bu header ile doğrulanır.

## Sistem Gereksinimleri

Bu uygulama ses dosyası işleme için **FFmpeg** gerektirir. Lütfen uygulamayı çalıştırmadan önce FFmpeg'i sisteminize kurun.

### FFmpeg Kurulumu

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. [ffmpeg.org](https://ffmpeg.org/download.html) adresinden Windows binary indirin
2. ZIP dosyasını çıkarın (örn: `C:\ffmpeg`)
3. `C:\ffmpeg\bin` klasörünü PATH environment variable'ına ekleyin

**Kurulumu Doğrulama:**
```bash
ffmpeg -version
```

Bu komut FFmpeg versiyonunu göstermelidir. Eğer "command not found" hatası alırsanız, FFmpeg PATH'e düzgün eklenmemiştir.

**Not:** Render deployment'ında FFmpeg otomatik olarak kurulur, sadece local development için manuel kurulum gereklidir.

## Hızlı Başlangıç

### 1) Otomatik kurulum (önerilen)

Local geliştirme ortamı için bağımlılıkları doğrulayan ve `.env` dosyalarını oluşturan script:

```bash
./setup-local.sh
```

Script FFmpeg/Python/Node.js kontrolü yapar, `backend/.venv` sanal ortamını kurar, `npm install` çalıştırır ve `.env` dosyalarını örneklerden kopyalar.

### 2) Manuel kurulum adımları

1. Ortam değişkenleri:
   ```bash
   cp .env.example .env
   cp frontend/.env.example frontend/.env
   ```
   - `APP_SECRET_TOKEN` (backend) ve `VITE_APP_SECRET_TOKEN` (frontend) değerleri **aynı** olmalıdır ve en az 32 karakterlik rastgele bir token olmalıdır.
   - `.env` dosyasında SMTP veya SendGrid alanlarını doldurarak e-posta gönderimini etkinleştirebilirsiniz.

2. Backend'i başlatın:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. Frontend'i başlatın:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Tarayıcıda `http://localhost:5173` adresine gidin. İlk ekrandaki katılımcı formunu doldurduktan sonra sohbet başlar; görüşme sonunda değerlendirme, rapor ve e-posta adımları UI üzerinden tetiklenebilir.

## 🚀 Render'a Deploy Etme

Proje Render üzerinde backend (FastAPI) + statik frontend olarak çalıştırılabilir. FFmpeg kurulumu `render.yaml` içinde otomatik yapılır.

1. Repo'yu Render hesabınıza bağlayın ve `render.yaml` dosyasıyla blueprint deploy başlatın.
2. `APP_SECRET_TOKEN`, `TARGET_EMAIL`, SMTP/SENDGRID alanları ve GPT API anahtarını Render ortam değişkenlerine ekleyin.
3. Deploy sonrası `/health` endpoint'i üzerinden sağlık durumunu doğrulayın.

Detaylı yönergeler için [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md) ve [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) dokümanlarını inceleyin.

## Testler

Backend birim ve entegrasyon testleri `tests/` klasöründedir. Çalıştırmak için:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt pytest
pytest
```

Testler; değerlendirme heuristiklerinin deterministik kalmasını, GPT istemcisi hata yakalama senaryolarını ve FastAPI uç noktalarının temel akışlarını doğrular.

## Proje Yapısı

```
backend/        # FastAPI uygulaması, servisler, model şemaları
frontend/       # React + Vite istemcisi ve UI bileşenleri
configs/        # TOEFL / iTEP / IELTS rubrik JSON dosyaları
docs/           # Şartname, mimari ve akış dokümanları
tests/          # Pytest senaryoları (API + değerlendirme)
```

## Standart Bazlı Değerlendirme

- UI, görüşmeyi interviewer rol mesajlarıyla yürütür ve oturum tamamlandığında backend `configs/*` altında tutulan JSON rubriklerine göre skor üretir.
- GPT-5 API anahtarı sağlandığında, gelen JSON çıktısı heuristik sonuçlarla birleştirilir; aksi halde yerleşik heuristikler tek başına kullanılır.
- Yeni standart eklemek için ilgili dizine `configs/<standard>/<version>.json` dosyası koymak yeterlidir; kriter isimleri otomatik olarak UI'da gösterilir.

## Ek Notlar

- JSON konfigürasyonları gerçekçi varsayılanlarla doldurulmuştur; skor ağırlıkları, CEFR eşlemeleri ve aksiyon planları bu dosyalardan okunur.
- Uygulama sabit metin yerine config ve servis katmanlarından beslenir; böylece yeni senaryoları kod değişmeden deneyebilirsiniz.
