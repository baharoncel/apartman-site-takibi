from django.db import models
from django.contrib.auth.models import User

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı Hesabı")
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    flat_number = models.CharField(max_length=10, verbose_name="Daire No", unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="Telefon", blank=True, null=True)
    email = models.EmailField(verbose_name="E-posta", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Profil Fotoğrafı")
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.user_id:
            username = f"daire{self.flat_number}"
            password = "password123" # Geçici şifre
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.first_name = self.first_name
                user.last_name = self.last_name
                user.email = self.email
                user.save()
            self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Daire: {self.flat_number})"
        
    class Meta:
        verbose_name = "Daire Sakini"
        verbose_name_plural = "Daire Sakinleri"

class Due(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, verbose_name="Daire Sakini", related_name="dues")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    issue_date = models.DateField(verbose_name="Kesim Tarihi")
    due_date = models.DateField(verbose_name="Son Ödeme Tarihi")
    is_paid = models.BooleanField(default=False, verbose_name="Ödendi mi?")
    
    def __str__(self):
        return f"{self.resident.first_name} {self.resident.last_name} - {self.amount} TL"
        
    class Meta:
        verbose_name = "Aidat"
        verbose_name_plural = "Aidatlar"
        ordering = ['-issue_date']

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('INCOME', 'Gelir'),
        ('EXPENSE', 'Gider'),
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="İşlem Tipi")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    description = models.TextField(verbose_name="Açıklama")
    date = models.DateField(auto_now_add=True, verbose_name="Tarih")
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name="Fatura / Fiş")
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} TL"
        
    class Meta:
        verbose_name = "Gelir/Gider İşlemi"
        verbose_name_plural = "Gelir/Gider İşlemleri"
        ordering = ['-date']

class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="Yayınlanma Tarihi")
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        ordering = ['-date_posted']

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Bekliyor'),
        ('RESOLVED', 'Çözüldü'),
    )
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, verbose_name="Daire Sakini", related_name="complaints")
    title = models.CharField(max_length=150, verbose_name="Konu / Başlık")
    description = models.TextField(verbose_name="Mesaj")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Durum")
    date_submitted = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    
    def __str__(self):
        return f"{self.resident.flat_number} - {self.title}"
        
    class Meta:
        verbose_name = "İstek / Şikayet"
        verbose_name_plural = "İstek ve Şikayetler"
        ordering = ['-date_submitted']

class Vehicle(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="vehicles", verbose_name="Daire Sakini")
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Plaka")
    brand_model = models.CharField(max_length=100, verbose_name="Marka / Model")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Renk")
    
    def __str__(self):
        return f"{self.license_plate} - {self.brand_model}"
        
    class Meta:
        verbose_name = "Araç"
        verbose_name_plural = "Araçlar"

class Poll(models.Model):
    question = models.CharField(max_length=255, verbose_name="Soru")
    end_date = models.DateTimeField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    def __str__(self):
        return self.question
        
    class Meta:
        verbose_name = "Anket"
        verbose_name_plural = "Anketler"

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200, verbose_name="Seçenek")
    votes = models.ManyToManyField(Resident, blank=True, related_name="voted_choices", verbose_name="Oy Verenler")
    
    def __str__(self):
        return self.choice_text
        
    @property
    def vote_count(self):
        return self.votes.count()

class Facility(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tesis Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Tesis"
        verbose_name_plural = "Tesisler"

class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="bookings", verbose_name="Tesis")
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="bookings", verbose_name="Daire Sakini")
    start_time = models.DateTimeField(verbose_name="Başlangıç Zamanı")
    end_time = models.DateTimeField(verbose_name="Bitiş Zamanı")
    
    def __str__(self):
        return f"{self.facility.name} - {self.resident.flat_number} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"
        
    class Meta:
        verbose_name = "Rezervasyon"
        verbose_name_plural = "Rezervasyonlar"
        ordering = ['-start_time']

class Visitor(models.Model):
    VISITOR_TYPES = (
        ('GUEST', 'Misafir'),
        ('CARGO', 'Kargo / Teslimat'),
        ('SERVICE', 'Servis / Tamir'),
    )
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="visitors", verbose_name="Daire Sakini")
    visitor_name = models.CharField(max_length=150, verbose_name="Ziyaretçi / Firma Adı")
    visitor_type = models.CharField(max_length=15, choices=VISITOR_TYPES, default='GUEST', verbose_name="Tipi")
    arrival_time = models.DateTimeField(auto_now_add=True, verbose_name="Geliş Zamanı")
    
    def __str__(self):
        return f"{self.visitor_name} -> Daire {self.resident.flat_number}"
        
    class Meta:
        verbose_name = "Ziyaretçi / Kargo"
        verbose_name_plural = "Ziyaretçi ve Kargolar"
        ordering = ['-arrival_time']

class Staff(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    role = models.CharField(max_length=100, verbose_name="Görevi")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maaş", blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
        
    class Meta:
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"

class Inventory(models.Model):
    item_name = models.CharField(max_length=150, verbose_name="Demirbaş Adı")
    location = models.CharField(max_length=150, verbose_name="Bulunduğu Yer")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Alım Tarihi")
    warranty_end = models.DateField(blank=True, null=True, verbose_name="Garanti Bitiş")
    
    def __str__(self):
        return self.item_name
        
    class Meta:
        verbose_name = "Demirbaş"
        verbose_name_plural = "Demirbaşlar"

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Belge Adı")
    file = models.FileField(upload_to='documents/', verbose_name="Dosya")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Belge / Karar Defteri"
        verbose_name_plural = "Belgeler"

class MessageBoard(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="messages", verbose_name="Sakin")
    content = models.TextField(verbose_name="Mesaj")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    
    def __str__(self):
        return f"{self.resident.first_name}: {self.content[:30]}..."
        
    class Meta:
        verbose_name = "İlan / Mesaj"
        verbose_name_plural = "Mesaj Panosu"
        ordering = ['-timestamp']

class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Bekliyor'),
        ('IN_PROGRESS', 'Yapılıyor'),
        ('DONE', 'Tamamlandı'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="tasks", verbose_name="Görevli Personel")
    title = models.CharField(max_length=200, verbose_name="Görev Başlığı")
    description = models.TextField(verbose_name="Görev Detayı")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Durum")
    date_assigned = models.DateTimeField(auto_now_add=True, verbose_name="Atanma Tarihi")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Görev / İş Emri"
        verbose_name_plural = "Görevler"

class Pet(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="pets", verbose_name="Daire Sakini")
    pet_name = models.CharField(max_length=100, verbose_name="Evcil Hayvan Adı")
    pet_type = models.CharField(max_length=100, verbose_name="Türü / Cinsi")
    notes = models.TextField(blank=True, verbose_name="Aşı / Özel Notlar")
    
    def __str__(self):
        return f"{self.pet_name} ({self.pet_type})"
        
    class Meta:
        verbose_name = "Evcil Hayvan"
        verbose_name_plural = "Evcil Hayvanlar"

class Supplier(models.Model):
    company_name = models.CharField(max_length=200, verbose_name="Firma Adı")
    category = models.CharField(max_length=100, verbose_name="Kategori (Asansör, Tesisat vb.)")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="İlgili Kişi")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    
    def __str__(self):
        return f"{self.company_name} - {self.category}"
        
    class Meta:
        verbose_name = "Tedarikçi / Acil Durum"
        verbose_name_plural = "Firma ve Tedarikçiler"

class MarketplaceItem(models.Model):
    ITEM_TYPES = (
        ('FOR_SALE', 'Satılık'),
        ('FOR_RENT', 'Kiralık'),
        ('FREE', 'Ücretsiz / Bağış'),
    )
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="marketplace_items", verbose_name="İlan Sahibi")
    title = models.CharField(max_length=150, verbose_name="İlan Başlığı")
    description = models.TextField(verbose_name="Açıklama")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Fiyat (TL)")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='FOR_SALE', verbose_name="İlan Tipi")
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True, verbose_name="Ürün Fotoğrafı")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="İletişim Numarası")
    is_sold = models.BooleanField(default=False, verbose_name="Satıldı / Kapandı mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yayın Tarihi")

    def __str__(self):
        return f"{self.title} ({self.get_item_type_display()})"

    class Meta:
        verbose_name = "Pazar İlanı"
        verbose_name_plural = "Komşu Pazarı / 2. El İlanlar"
        ordering = ['-created_at']

class EmergencyAlert(models.Model):
    SEVERITY_CHOICES = (
        ('INFO', 'Bilgilendirme'),
        ('WARNING', 'Uyarı / Kesinti'),
        ('DANGER', 'Kritik Acil Durum'),
    )
    title = models.CharField(max_length=150, verbose_name="Başlık")
    message = models.TextField(verbose_name="Mesaj / Detay")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='WARNING', verbose_name="Önem Seviyesi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"

    class Meta:
        verbose_name = "Acil Durum / Uyarı"
        verbose_name_plural = "Acil Durum & Kesinti Bildirimleri"
        ordering = ['-created_at']

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=Notice)
def send_notice_email(sender, instance, created, **kwargs):
    if created:
        emails = [r.email for r in Resident.objects.exclude(email__isnull=True).exclude(email__exact='')]
        if emails:
            send_mail(
                subject=f"Yeni Duyuru: {instance.title}",
                message=f"Merhaba,\n\nYeni bir duyuru yayınlandı:\n\n{instance.content}\n\nİyi günler dileriz.",
                from_email='yonetim@aidatpro.com',
                recipient_list=emails,
                fail_silently=True,
            )
