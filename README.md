<div align="center">

# 🏢 AidatPro - Akıllı Apartman & Site Yönetim Otomasyonu

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-6.0-green.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-F5788D.svg?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <strong>Modern, şeffaf ve kapsamlı bir apartman & site yönetim ekosistemi.</strong><br>
  Finansal analizler, online aidat ve kasa takibi, resmi dekont üretimi, komşu pazarı vitrini, acil durum bildirimleri ve sosyal tesis rezervasyonları tek bir çatı altında.
</p>

</div>

---

## 📸 Ekran Görüntüleri & Özellikler

| Yönetici Finans Dashboard'u | Komşu Pazarı (2. El Vitrini) |
| :---: | :---: |
| *Aylık Gelir-Gider Bar & Donut Grafikleri* | *Sakinlerin ilan paylaştığı pazar yeri* |
| **Resmi Aidat Tahsilat Makbuzu** | **Daire Sakini Portalı & Ödemeler** |
| *Yazdırılabilir ve PDF uyumlu elektronik dekont* | *Kişisel borç durumu ve tesis rezervasyonları* |

---

## 🚀 Öne Çıkan Özellikler

### 📊 1. Finansal Analitik & Raporlama
* **İnteraktif Grafikler (Chart.js):** Son 6 ayın gelir-gider trendi ve aidat tahsilat oranı grafikleri.
* **Resmi Aidat Makbuzu / Dekont Üretimi:** Her ödeme işlemi için elektronik onaylı, yazdırılabilir ve PDF'e aktarılabilir resmi tahsilat makbuzu (`/aidat/<id>/makbuz/`).
* **Excel / CSV Dışa Aktarma:** Tek tıkla aidat borçluları listesi ve kasa hareketleri dökümü indirme.
* **Toplu Aidat Tanımlama:** Tek form ile sitedeki tüm dairelere anında aylık aidat borcu yansıtma.

### 🛒 2. Komşu Pazarı (2. El Eşya & İlanlar)
* Sakinlerin satılık, kiralık veya ücretsiz eşyalarını fotoğraflı olarak yayınlayabildiği modern vitrin.
* Durum güncellemesi (Satıldı/Kapandı) ve anlık tip filtreleme (Satılık, Kiralık, Bağış).

### 🚨 3. Acil Durum & Kesinti Bildirim Merkezi
* Su, elektrik, doğalgaz kesintileri veya kritik arızalar için anlık bildirim bandı (Banner & Ticker).
* Önem derecesine göre renk kodlu uyarılar (Kritik, Uyarı, Bilgilendirme).

### 🏡 4. Site & Topluluk Modülleri
* **Sosyal Tesis Rezervasyon Sistemi:** Tenis kortu, havuz, sauna vb. çakışma önleyici akıllı rezervasyon.
* **Araç & Plaka Yönetimi:** Otopark ve güvenlik kontrolü için sakin araç kayıtları.
* **Kargo & Ziyaretçi Takibi:** Güvenlik kapısı giriş-çıkış logları.
* **Evcil Hayvan Kayıtları:** Aşı ve künye bilgileriyle site içi can dostlarımızın takibi.
* **Personel & İş Emirleri:** Görev atama, durum takibi (Bekliyor, Yapılıyor, Tamamlandı).
* **Demirbaş Envanteri:** Garanti süreleri ve demirbaş lokasyonları.
* **Anket & Oylama:** Site sakinlerinin kararlara katılımını sağlayan online oylama modülü.
* **İstek & Şikayet Yönetimi:** Sakinlerin yönetime ilettiği talepler ve durum takibi.

### 👤 5. Sakin Portalı & Profil Yönetimi
* Profil fotoğrafı yükleme, iletişim bilgisi güncelleme.
* Güvenli şifre değiştirme paneli.
* Sakinin araçları, evcil hayvanları ve aktif rezervasyonlarını tek ekranda toplayan yönetim sayfası.
* **🌓 Karanlık / Aydınlık Mod:** Gözü yormayan modern Dark Theme desteği.

---

## 🛠️ Teknoloji Yığını

* **Backend:** Python 3.10+, Django 6.0
* **Frontend:** HTML5, CSS3 (Modern Glassmorphism & Custom Design System), Vanilla JS
* **Görselleştirme:** Chart.js
* **Veritabanı:** SQLite (Geliştirme) / PostgreSQL (Üretim uyumlu)
* **İletişim & Bildirim:** Django Signals & Console Email Backend

---

## ⚡ Hızlı Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/baharoncel/apartman-site-takibi.git
cd apartman-site-takibi
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python3 -m venv env
source env/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veritabanını Hazırlayın & Örnek Verileri Yükleyin
```bash
python manage.py migrate
python seed_data.py
```
> `seed_data.py` scripti tüm daireleri, örnek aidatları, kasa hareketlerini, ilanları ve test hesaplarını otomatik oluşturur.

### 5. Sunucuyu Başlatın
```bash
python manage.py runserver
```

Tarayıcınızda açın: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔑 Hazır Test Kullanıcı Girişleri

| Rol | Kullanıcı Adı | Şifre | Açıklama |
| :--- | :--- | :--- | :--- |
| **👑 Yönetici** | `admin` | `admin123` | Tam yetkili site yönetici paneli |
| **👤 Daire 1 Sakini** | `daire1` | `password123` | Ahmet Yılmaz (Borçlu daire) |
| **👤 Daire 2 Sakini** | `daire2` | `password123` | Ayşe Demir (Ödemeleri düzenli) |
| **👤 Daire 3 Sakini** | `daire3` | `password123` | Mehmet Kaya |

---

## 📁 Proje Dizin Yapısı

```plaintext
├── aidat_takip/          # Django Proje Ayarları (settings, urls, wsgi)
├── core/                 # Ana Uygulama (Modeller, View'lar, Formlar, Admin)
│   ├── models.py         # 15+ İlişkisel Veritabanı Modeli
│   ├── views.py          # Analitik, CRUD, CSV Export ve Rapor Görünümleri
│   ├── forms.py          # Dinamik Formlar ve Validasyonlar
│   ├── urls.py           # RESTful URL Rotaları
│   └── admin.py          # Kapsamlı Django Admin Yapılandırması
├── static/               # CSS Tasarım Sistemi, JS ve Varlıklar
│   ├── styles.css        # Responsive Glassmorphism & Dark Mode Stilleri
│   └── scripts.js        # Canlı Arama ve Tema Yönetimi
├── templates/            # 30+ Jinja/Django HTML Şablonu
│   ├── base.html         # Ortak Arayüz İskeleti ve Bildirimler
│   ├── dashboard.html    # Chart.js Grafikli Ana Panel
│   ├── receipt.html      # Yazdırılabilir Aidat Makbuzu
│   ├── marketplace.html  # Komşu Pazarı Vitrini
│   └── profile.html      # Sakin Profil & Ayarlar
├── requirements.txt      # Gerekli Python Kütüphaneleri
├── seed_data.py          # Otomatik Demo Veri Oluşturucu
└── README.md             # Proje Dokümantasyonu
```

---

## 🤝 Katkıda Bulunma

1. Bu depoyu Fork'layın (`Fork` butonuna basın)
2. Yeni bir Özellik Dalı (Feature Branch) oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi Commit edin (`git commit -m 'feat: Yeni özellik eklendi'`)
4. Dalınıza Push yapın (`git push origin feature/YeniOzellik`)
5. Bir Pull Request (PR) açın

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır.
