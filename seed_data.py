import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aidat_takip.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from core.models import (
    Resident, Due, Transaction, Notice, Complaint, Vehicle, Poll, Choice,
    Facility, Booking, Visitor, Staff, Inventory, Document, MessageBoard,
    Task, Pet, Supplier, MarketplaceItem, EmergencyAlert
)

def run_seed():
    print("🌱 Veritabanı tohumlama (Seed Data) başlatılıyor...")

    # 1. Superuser
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@aidatpro.com', 'first_name': 'Site', 'last_name': 'Yöneticisi', 'is_staff': True, 'is_superuser': True})
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Yönetici kullanıcısı oluşturuldu (admin / admin123)")
    else:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

    # 2. Residents
    residents_data = [
        ("Ahmet", "Yılmaz", "1", "0532 111 2233", "ahmet@gmail.com"),
        ("Ayşe", "Demir", "2", "0542 222 3344", "ayse@gmail.com"),
        ("Mehmet", "Kaya", "3", "0555 333 4455", "mehmet@gmail.com"),
        ("Fatma", "Şahin", "4", "0533 444 5566", "fatma@gmail.com"),
        ("Mustafa", "Çelik", "5", "0544 555 6677", "mustafa@gmail.com"),
        ("Zeynep", "Yıldız", "6", "0505 666 7788", "zeynep@gmail.com"),
        ("Emre", "Öztürk", "7", "0530 777 8899", "emre@gmail.com"),
        ("Burcu", "Aydın", "8", "0540 888 9900", "burcu@gmail.com"),
    ]

    residents = []
    for fn, ln, flat, phone, email in residents_data:
        r, created = Resident.objects.get_or_create(
            flat_number=flat,
            defaults={'first_name': fn, 'last_name': ln, 'phone_number': phone, 'email': email}
        )
        if created:
            # User automatically created by model save()
            pass
        residents.append(r)
    print(f"✅ {len(residents)} adet daire sakini ve kullanıcı hesabı hazır.")

    # 3. Dues (Aidatlar)
    today = timezone.now().date()
    months_back = [today - timedelta(days=30*i) for i in range(3)]
    
    for r_idx, r in enumerate(residents):
        for m_idx, m_date in enumerate(months_back):
            issue_d = m_date.replace(day=1)
            due_d = m_date.replace(day=15)
            is_paid = True if (m_idx > 0 or r_idx % 2 == 0) else False
            
            Due.objects.get_or_create(
                resident=r,
                issue_date=issue_d,
                defaults={'amount': Decimal('750.00'), 'due_date': due_d, 'is_paid': is_paid}
            )
    print("✅ Geçmiş ve güncel aidat kayıtları oluşturuldu.")

    # 4. Transactions (Kasa Gelir / Giderleri)
    tx_data = [
        ('INCOME', Decimal('6000.00'), 'Ocak Ayı Toplu Aidat Tahsilatları', today - timedelta(days=60)),
        ('EXPENSE', Decimal('1850.00'), 'Ortak Alan Elektrik ve Aydınlatma Faturası', today - timedelta(days=55)),
        ('EXPENSE', Decimal('1200.00'), 'Asansör Aylık Periyodik Bakım Bedeli', today - timedelta(days=45)),
        ('INCOME', Decimal('5250.00'), 'Şubat Ayı Aidat Tahsilatları', today - timedelta(days=30)),
        ('EXPENSE', Decimal('950.00'), 'Bahçe ve Çevre Düzenleme İlaçlama', today - timedelta(days=25)),
        ('EXPENSE', Decimal('2200.00'), 'Temizlik Görevlisi SGK ve Avans Ödemesi', today - timedelta(days=20)),
        ('INCOME', Decimal('4500.00'), 'Mart Ayı Aidat Girişleri', today - timedelta(days=5)),
        ('EXPENSE', Decimal('650.00'), 'Ortak Alan Su Faturası', today - timedelta(days=3)),
    ]
    for t_type, amt, desc, t_date in tx_data:
        tx, created = Transaction.objects.get_or_create(
            description=desc,
            defaults={'transaction_type': t_type, 'amount': amt}
        )
        if created:
            tx.date = t_date
            tx.save()
    print("✅ Kasa gelir/gider hareketleri eklendi.")

    # 5. Emergency Alerts & Notices
    EmergencyAlert.objects.get_or_create(
        title="Planlı Su Kesintisi",
        defaults={
            'message': "İSKİ ana boru yenileme çalışması nedeniyle Çarşamba 13:00 - 17:00 arası sular kesilecektir. Lütfen tedbir alınız.",
            'severity': 'WARNING',
            'is_active': True
        }
    )
    EmergencyAlert.objects.get_or_create(
        title="B Blok Asansör Revizyonu",
        defaults={
            'message': "B Blok 2 No'lu asansörün halat değişimi yapılmaktadır. Gün boyu hizmet dışıdır.",
            'severity': 'INFO',
            'is_active': True
        }
    )

    Notice.objects.get_or_create(
        title="2026 Yılı Olağan Genel Kurul Toplantısı",
        defaults={'content': "Değerli site sakinlerimiz, yıllık olağan genel kurul toplantımız 15 Mart Pazar günü saat 14:00'te sosyal tesiste yapılacaktır. Katılımınız önemle rica olunur."}
    )
    Notice.objects.get_or_create(
        title="Yaz Sezonu Havuz & Tesis Kullanım Kuralları",
        defaults={'content': "Açık havuzumuz bakım ve klorlama sonrası hizmete açılmıştır. Girişlerde lütfen rezervasyon sistemini kullanınız."}
    )
    print("✅ Acil durum uyarıları ve site duyuruları eklendi.")

    # 6. Marketplace Items (2. El Pazar Yeri)
    MarketplaceItem.objects.get_or_create(
        title="Chicco Bebek Arabası (Çok Temiz)",
        resident=residents[0],
        defaults={
            'description': "Az kullanılmış, katlanabilir, çift yönlü pusetli bebek arabası.",
            'price': Decimal('1450.00'),
            'item_type': 'FOR_SALE',
            'contact_phone': '0532 111 2233',
            'is_sold': False
        }
    )
    MarketplaceItem.objects.get_or_create(
        title="İkea Ahşap Çalışma Masası",
        resident=residents[1],
        defaults={
            'description': "Taşınma sebebiyle acil satılık, 120x60 cm tertemiz masa.",
            'price': Decimal('750.00'),
            'item_type': 'FOR_SALE',
            'contact_phone': '0542 222 3344',
            'is_sold': False
        }
    )
    MarketplaceItem.objects.get_or_create(
        title="Üniversite Hazırlık & Roman Kitap Seti",
        resident=residents[2],
        defaults={
            'description': "İhtiyacı olan komşularımızın çocuklarına ücretsiz hediye edilecektir.",
            'price': None,
            'item_type': 'FREE',
            'contact_phone': '0555 333 4455',
            'is_sold': False
        }
    )
    print("✅ Komşu pazarı vitrini için örnek ilanlar eklendi.")

    # 7. Facilities & Bookings
    f1, _ = Facility.objects.get_or_create(name="Tenis Kortu", defaults={'description': 'Işıklandırmalı açık tenis kortu (Rezervasyon zorunludur)'})
    f2, _ = Facility.objects.get_or_create(name="Kapalı Yüzme Havuzu & Sauna", defaults={'description': 'Haftanın 6 günü 08:00 - 22:00 arası açık.'})
    f3, _ = Facility.objects.get_or_create(name="Barbekü & Kamelya Alanı", defaults={'description': 'Site içi özel etkinlik ve mangal alanı.'})

    Booking.objects.get_or_create(
        facility=f1,
        resident=residents[0],
        start_time=timezone.now() + timedelta(days=1, hours=2),
        defaults={'end_time': timezone.now() + timedelta(days=1, hours=3)}
    )

    # 8. Staff & Tasks
    s1, _ = Staff.objects.get_or_create(first_name="Kemal", last_name="Usta", role="Teknik Personel", defaults={'phone': '0535 999 8877', 'salary': Decimal('22000.00')})
    s2, _ = Staff.objects.get_or_create(first_name="Gülten", last_name="Hanım", role="Temizlik & Düzen", defaults={'phone': '0545 888 7766', 'salary': Decimal('19000.00')})

    Task.objects.get_or_create(
        staff=s1,
        title="A Blok Hidrofor Basınç Kontrolü",
        defaults={'description': 'Su basıncı dalgalanması kontrol edilecek, vana contaları yenilenecek.', 'status': 'IN_PROGRESS'}
    )
    Task.objects.get_or_create(
        staff=s2,
        title="Kapalı Otopark Zemin Yıkaması",
        defaults={'description': 'Haftalık program dahilinde -1 ve -2 otopark yıkanacak.', 'status': 'PENDING'}
    )

    # 9. Vehicles, Pets, Suppliers
    Vehicle.objects.get_or_create(license_plate="34 ABC 789", resident=residents[0], defaults={'brand_model': 'Toyota Corolla', 'color': 'Beyaz'})
    Vehicle.objects.get_or_create(license_plate="34 XYZ 123", resident=residents[1], defaults={'brand_model': 'Volkswagen Golf', 'color': 'Gri'})
    
    Pet.objects.get_or_create(pet_name="Pamuk", resident=residents[0], defaults={'pet_type': 'British Shorthair Kedi', 'notes': 'Aşıları tam, çipli.'})
    Pet.objects.get_or_create(pet_name="Rüzgar", resident=residents[2], defaults={'pet_type': 'Golden Retriever Köpek', 'notes': 'Uysal ve eğitimli.'})

    Supplier.objects.get_or_create(company_name="Kone Asansör Servisi", category="Asansör Bakım / 7-24 Acil", defaults={'phone': '0212 444 0 567', 'contact_person': 'Murat Bey'})
    Supplier.objects.get_or_create(company_name="Mavi Tesisat & Kalorifer", category="Sıhhi Tesisat / Doğalgaz", defaults={'phone': '0532 999 0011', 'contact_person': 'Hasan Usta'})
    Supplier.objects.get_or_create(company_name="Site Güvenlik & Kamera", category="Güvenlik Sistemleri", defaults={'phone': '0216 333 4455', 'contact_person': 'Engin Bey'})

    # 10. Polls
    poll, p_created = Poll.objects.get_or_create(
        question="Site Bahçesine Elektrikli Araç (EV) Şarj İstasyonu Kurulsun mu?",
        defaults={'end_date': timezone.now() + timedelta(days=15), 'is_active': True}
    )
    if p_created:
        Choice.objects.create(poll=poll, choice_text="Evet, kurulsun (Gereklilik)")
        Choice.objects.create(poll=poll, choice_text="Hayır, gerek yok")
        Choice.objects.create(poll=poll, choice_text="Maliyete göre karar verilsin")

    print("\n🎉 Tebrikler! Tüm demo ve test verileri başarıyla yüklendi!")
    print("=" * 60)
    print("🔑 TEST HESAPLARI:")
    print("  👑 Yönetici Girişi : Kullanıcı: admin   | Şifre: admin123")
    print("  👤 Sakin Girişi    : Kullanıcı: daire1  | Şifre: password123")
    print("  👤 Sakin Girişi 2  : Kullanıcı: daire2  | Şifre: password123")
    print("=" * 60)

if __name__ == '__main__':
    run_seed()
