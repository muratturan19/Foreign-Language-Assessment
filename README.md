# Foreign Language Assessment Platform

Tamamlanmış bu proje, TOEFL-benzeri kriterlere göre konuşma değerlendirmesi yapan İngilizce mülakat koçu deneyimini uçtan uca sağlar. Uygulama iki ana bileşenden oluşur:

- **Backend (FastAPI)** – Oturum yönetimi, değerlendirme motoru, rapor üretimi ve e-posta kuyruklama uçlarını sunar.
- **Frontend (React + Vite)** – Metin tabanlı sohbet arayüzü, oturum kontrolü ve değerlendirme sonuçlarının görselleştirilmesini sağlar.

Ayrıntılı gereksinimler için [docs/SPEC.md](docs/SPEC.md) belgesine bakabilirsiniz.

## Hızlı Başlangıç

### 1. Ortamı Hazırlayın

```
cp .env.example .env
cp frontend/.env.example frontend/.env
```

`.env` dosyasında gizli anahtarları ve e-posta yapılandırmasını güncelleyin. `APP_SECRET_TOKEN` değeri artık zorunludur ve en az 32 karakterden oluşan güçlü bir anahtar olmalıdır; uygulama bu değişken tanımlanmadan veya varsayılan `dev-secret` değeri kullanılırsa başlatılamaz. Backend ve frontend aynı anahtarı paylaşmalıdır.

Güvenli bir token oluşturmak için aşağıdaki komutlardan birini kullanabilirsiniz:
```bash
# Python kullanarak
python -c "import secrets; print(secrets.token_urlsafe(32))"

# veya OpenSSL kullanarak
openssl rand -base64 32
```

### 2. Backend'i Çalıştırın

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API varsayılan olarak `http://localhost:8000` adresinde ayağa kalkar. Sağlık kontrolü için `/health` uç noktasını kullanabilirsiniz.

### 3. Frontend'i Çalıştırın

```bash
cd frontend
npm install
npm run dev
```

Geliştirme sunucusu `http://localhost:5173` adresinde çalışır ve API isteklerini Vite proxy üzerinden backend'e yönlendirir.

## 🚀 Render'a Deploy Etme

Bu uygulama Render platformunda kolayca deploy edilebilir. Tüm fonksiyonlar (email gönderme, ses dosyası işleme) çalışır.

### Hızlı Başlangıç

1. Repository'yi Render'a bağlayın
2. Environment variables'ları ekleyin (APP_SECRET_TOKEN, email ayarları, GPT API key)
3. Deploy edin (otomatik FFmpeg kurulumu ve frontend build)

**Detaylı rehber**: [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md)
**Kapsamlı dokümantasyon**: [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)

### Özellikler

- ✅ FFmpeg ile otomatik ses dosyası işleme
- ✅ SMTP/SendGrid email entegrasyonu
- ✅ Persistent disk ile audio/report saklama
- ✅ Health check ve auto-deploy
- ✅ React frontend static serving

## Testler

Backend testlerini çalıştırmak için depo kök dizinindeyken:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt pytest
pytest
```

Test paketi, değerlendirme servisinin deterministik sonuçlar döndürdüğünü ve temel API akışının beklendiği gibi çalıştığını doğrular.

## Proje Yapısı

```
backend/        # FastAPI uygulaması ve servis katmanı
docs/           # Proje şartnamesi
frontend/       # React + Vite istemcisi
tests/          # Pytest tabanlı backend testleri
```

## Özellikler

- TOEFL rubriğine göre 4 boyutlu (Delivery, Language Use, Topic Development, Task Fulfillment) değerlendirme
- CEFR seviye eşlemesi ve kişiselleştirilmiş 30 günlük aksiyon planı
- HTML raporu dosyaya kaydetme ve paylaşılabilir bağlantı üretme
- Mock e-posta gönderimi (SMTP/SendGrid entegrasyonuna hazır arayüz)
- React tabanlı sohbet arayüzü, oturum yönetimi ve değerlendirme sunumu

## Standart Bazlı Değerlendirme Taslağı
- Amaç: UI üzerinden değerlendirme standardı seçildiğinde ilgili JSON yüklenir; sohbet interviewer rolüyle ilerler, oturum bitince evaluator JSON'daki rubriğe göre puanlama yapar, CEFR eşlemesi ve HTML rapor hazırlanır, e-posta iletilir.
- Mevcut aşama: Kod yok; yalnızca tasarım dokümantasyonu ve dummy JSON konfigürasyonları bulunur.
- Gelecek faz: Frontend dropdown seçimleri backend'e ileterek ilgili JSON'u yükleyecek ve LLM'e aktaracak.

## Notlar
- JSON dosyaları placeholder içeriğe sahiptir; gerçek rubrik ve haritalama değerleri daha sonra doldurulacaktır.
- Uygulama kodu geliştirilirken sabit metin kullanılmayacak; tüm rol mesajları, kriterler, ağırlıklar ve CEFR eşlemesi JSON üzerinden okunacaktır.
- Yeni standart eklemek yalnızca `configs/<standard>/<version>.json` dosyası eklemeyi gerektirir.
