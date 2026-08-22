from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.MainDashboardView.as_view(), name='dashboard'),
    path('yonetici/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # Sakinler & Aidatlar & Finans
    path('sakinler/', views.ResidentListView.as_view(), name='residents'),
    path('aidatlar/', views.DueListView.as_view(), name='dues'),
    path('aidatlar/toplu-olustur/', views.BulkDueCreateView.as_view(), name='bulk_due_create'),
    path('aidatlar/export/csv/', views.export_dues_csv, name='export_dues_csv'),
    path('aidat/<int:pk>/ode/', views.DuePayView.as_view(), name='pay_due'),
    path('aidat/<int:pk>/makbuz/', views.ReceiptView.as_view(), name='receipt_view'),
    
    path('finans/', views.TransactionListView.as_view(), name='transactions'),
    path('finans/islem-ekle/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('finans/export/csv/', views.export_transactions_csv, name='export_transactions_csv'),
    
    # Komşu Pazarı (Marketplace)
    path('pazar/', views.MarketplaceListView.as_view(), name='marketplace'),
    path('pazar/ilan-ver/', views.MarketplaceCreateView.as_view(), name='marketplace_create'),
    path('pazar/<int:pk>/durum/', views.MarketplaceToggleSoldView.as_view(), name='marketplace_toggle'),
    
    # Acil Durum & Uyarılar
    path('acil-durumlar/', views.EmergencyAlertListView.as_view(), name='emergency_alerts'),
    path('acil-durum/ekle/', views.EmergencyAlertCreateView.as_view(), name='emergency_alert_create'),
    path('acil-durum/<int:pk>/durum/', views.EmergencyAlertToggleView.as_view(), name='emergency_alert_toggle'),
    
    # Profil & Güvenlik
    path('profil/', views.ProfileView.as_view(), name='profile'),
    path('sifre-degistir/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    
    # Duyurular & Şikayetler & Panolar & Anketler
    path('duyurular/', views.NoticeListView.as_view(), name='notices'),
    path('sikayetler/', views.ComplaintListView.as_view(), name='complaints'),
    path('sikayet-yaz/', views.ComplaintCreateView.as_view(), name='complaint_create'),
    path('sikayetler/<int:pk>/coz/', views.ComplaintResolveView.as_view(), name='complaint_resolve'),
    path('anketler/', views.PollListView.as_view(), name='polls'),
    path('anket/<int:poll_id>/oy/', views.vote_poll, name='vote_poll'),
    path('mesajlar/', views.MessageBoardListView.as_view(), name='messages'),
    path('mesaj-yaz/', views.MessageCreateView.as_view(), name='message_create'),
    
    # Tesisler & Araçlar & Ziyaretçiler & Personel & Demirbaş & Belgeler & Rehber
    path('tesisler/', views.FacilityListView.as_view(), name='facilities'),
    path('tesis/<int:facility_id>/rezervasyon/', views.BookingCreateView.as_view(), name='booking_create'),
    path('araclar/', views.VehicleListView.as_view(), name='vehicles'),
    path('arac-ekle/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('ziyaretciler/', views.VisitorListView.as_view(), name='visitors'),
    path('ziyaretci-ekle/', views.VisitorCreateView.as_view(), name='visitor_create'),
    path('personeller/', views.StaffListView.as_view(), name='staff'),
    path('gorevler/', views.TaskListView.as_view(), name='tasks'),
    path('gorevler/ekle/', views.TaskCreateView.as_view(), name='task_create'),
    path('gorevler/<int:pk>/durum/', views.TaskStatusUpdateView.as_view(), name='task_status_update'),
    path('demirbaslar/', views.InventoryListView.as_view(), name='inventory'),
    path('belgeler/', views.DocumentListView.as_view(), name='documents'),
    path('evcil-hayvanlar/', views.PetListView.as_view(), name='pets'),
    path('evcil-hayvan-ekle/', views.PetCreateView.as_view(), name='pet_create'),
    path('rehber/', views.SupplierListView.as_view(), name='suppliers'),
]
