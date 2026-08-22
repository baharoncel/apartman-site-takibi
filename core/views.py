import csv
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, FormView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    Resident, Due, Transaction, Notice, Complaint, Vehicle, Poll, Choice, 
    Facility, Booking, Visitor, Staff, Inventory, Document, MessageBoard, 
    Task, Pet, Supplier, MarketplaceItem, EmergencyAlert
)
from .forms import (
    BulkDueForm, TransactionForm, TaskForm, BookingForm,
    MarketplaceItemForm, EmergencyAlertForm, ResidentProfileForm
)

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class MainDashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.is_staff:
            return ['dashboard.html']
        return ['resident_dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Active Emergency Alerts
        context['active_alerts'] = EmergencyAlert.objects.filter(is_active=True).order_by('-created_at')[:3]
        
        if self.request.user.is_staff:
            paid_dues_total = Due.objects.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
            unpaid_dues_total = Due.objects.filter(is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
            total_income = Transaction.objects.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
            total_expense = Transaction.objects.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
            
            context['unpaid_dues_total'] = unpaid_dues_total
            context['paid_dues_total'] = paid_dues_total
            context['total_income'] = total_income
            context['total_expense'] = total_expense
            context['net_balance'] = total_income - total_expense
            context['recent_notices'] = Notice.objects.all()[:3]
            context['recent_transactions'] = Transaction.objects.all()[:5]
            context['open_complaints_count'] = Complaint.objects.filter(status='PENDING').count()
            context['recent_marketplace'] = MarketplaceItem.objects.filter(is_sold=False)[:4]

            # Chart Data - Monthly Income vs Expense (Last 6 Months)
            labels = []
            income_data = []
            expense_data = []
            now = timezone.now().date()
            for i in range(5, -1, -1):
                # Calculate month date
                year = now.year
                month = now.month - i
                while month <= 0:
                    month += 12
                    year -= 1
                month_start = datetime(year, month, 1).date()
                if month == 12:
                    next_month_start = datetime(year + 1, 1, 1).date()
                else:
                    next_month_start = datetime(year, month + 1, 1).date()
                
                month_name = month_start.strftime("%B %Y")
                labels.append(month_name)
                
                inc = Transaction.objects.filter(
                    transaction_type='INCOME', 
                    date__gte=month_start, 
                    date__lt=next_month_start
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                
                exp = Transaction.objects.filter(
                    transaction_type='EXPENSE', 
                    date__gte=month_start, 
                    date__lt=next_month_start
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                
                income_data.append(float(inc))
                expense_data.append(float(exp))

            context['chart_labels_json'] = json.dumps(labels)
            context['chart_income_json'] = json.dumps(income_data)
            context['chart_expense_json'] = json.dumps(expense_data)
            context['chart_dues_status_json'] = json.dumps([float(paid_dues_total), float(unpaid_dues_total)])

        else:
            try:
                resident = self.request.user.resident
                context['my_dues'] = Due.objects.filter(resident=resident).order_by('-issue_date')[:5]
                context['my_unpaid'] = Due.objects.filter(resident=resident, is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
                context['my_paid'] = Due.objects.filter(resident=resident, is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
                context['recent_notices'] = Notice.objects.all()[:3]
                context['recent_marketplace'] = MarketplaceItem.objects.filter(is_sold=False)[:4]
            except (Resident.DoesNotExist, AttributeError):
                context['my_unpaid'] = 0
                context['my_paid'] = 0
                context['recent_marketplace'] = MarketplaceItem.objects.filter(is_sold=False)[:4]

        return context

class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Complaint.objects.all()
        try:
            return Complaint.objects.filter(resident=self.request.user.resident)
        except (Resident.DoesNotExist, AttributeError):
            return Complaint.objects.none()

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    template_name = 'complaint_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('complaints')
    
    def form_valid(self, form):
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class ResidentListView(LoginRequiredMixin, ListView):
    model = Resident
    template_name = 'residents.html'
    context_object_name = 'residents'

class DueListView(LoginRequiredMixin, ListView):
    model = Due
    template_name = 'dues.html'
    context_object_name = 'dues'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Due.objects.all().select_related('resident')
        try:
            return Due.objects.filter(resident=self.request.user.resident)
        except (Resident.DoesNotExist, AttributeError):
            return Due.objects.none()

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions.html'
    context_object_name = 'transactions'

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices.html'
    context_object_name = 'notices'

class DuePayView(LoginRequiredMixin, TemplateView):
    template_name = 'pay_due.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        due = get_object_or_404(Due, pk=self.kwargs['pk'])
        if not self.request.user.is_staff and hasattr(self.request.user, 'resident'):
            if due.resident != self.request.user.resident:
                due = None
        context['due'] = due
        return context

    def post(self, request, *args, **kwargs):
        due = get_object_or_404(Due, pk=self.kwargs['pk'])
        if not request.user.is_staff and hasattr(request.user, 'resident'):
            if due.resident != request.user.resident:
                return redirect('dashboard')
        due.is_paid = True
        due.save()
        
        # Also record automatically as an INCOME transaction in the kasası!
        Transaction.objects.create(
            transaction_type='INCOME',
            amount=due.amount,
            description=f"Aidat Tahsilatı: Daire {due.resident.flat_number} - {due.resident.first_name} {due.resident.last_name}"
        )
        
        messages.success(request, f"Daire {due.resident.flat_number} için {due.amount} TL aidat ödemesi başarıyla alındı!")
        return redirect('receipt_view', pk=due.pk)

class ReceiptView(LoginRequiredMixin, DetailView):
    model = Due
    template_name = 'receipt.html'
    context_object_name = 'due'

    def get_object(self, queryset=None):
        due = super().get_object(queryset)
        if not self.request.user.is_staff and hasattr(self.request.user, 'resident'):
            if due.resident != self.request.user.resident:
                return get_object_or_404(Due, pk=0)
        return due

class PollListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = 'polls.html'
    context_object_name = 'polls'
    
    def get_queryset(self):
        return Poll.objects.filter(is_active=True).order_by('-end_date')

def vote_poll(request, poll_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'resident'):
        return redirect('login')
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id)
            for c in poll.choices.all():
                c.votes.remove(request.user.resident)
            choice.votes.add(request.user.resident)
    return redirect('polls')

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles.html'
    context_object_name = 'vehicles'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Vehicle.objects.all()
        try:
            return Vehicle.objects.filter(resident=self.request.user.resident)
        except (Resident.DoesNotExist, AttributeError):
            return Vehicle.objects.none()

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'vehicle_form.html'
    fields = ['license_plate', 'brand_model', 'color']
    success_url = reverse_lazy('vehicles')
    
    def form_valid(self, form):
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class FacilityListView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = 'facilities.html'
    context_object_name = 'facilities'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('facilities')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['facility'] = get_object_or_404(Facility, pk=self.kwargs['facility_id'])
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facility'] = get_object_or_404(Facility, pk=self.kwargs['facility_id'])
        return context
        
    def form_valid(self, form):
        form.instance.facility = get_object_or_404(Facility, pk=self.kwargs['facility_id'])
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class VisitorListView(LoginRequiredMixin, ListView):
    model = Visitor
    template_name = 'visitors.html'
    context_object_name = 'visitors'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Visitor.objects.all()
        try:
            return Visitor.objects.filter(resident=self.request.user.resident)
        except (Resident.DoesNotExist, AttributeError):
            return Visitor.objects.none()

class VisitorCreateView(LoginRequiredMixin, CreateView):
    model = Visitor
    template_name = 'visitor_form.html'
    fields = ['visitor_name', 'visitor_type']
    success_url = reverse_lazy('visitors')
    
    def form_valid(self, form):
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff.html'
    context_object_name = 'staff_members'

class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'inventory.html'
    context_object_name = 'inventory_items'

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents.html'
    context_object_name = 'documents'
    
    def get_queryset(self):
        return Document.objects.all().order_by('-upload_date')

class MessageBoardListView(LoginRequiredMixin, ListView):
    model = MessageBoard
    template_name = 'message_board.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return MessageBoard.objects.all().order_by('-timestamp')

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = MessageBoard
    template_name = 'message_form.html'
    fields = ['content']
    success_url = reverse_lazy('messages')
    
    def form_valid(self, form):
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class AdminDashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_collected = Transaction.objects.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Transaction.objects.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        unpaid_dues = Due.objects.filter(is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
        paid_dues = Due.objects.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        open_complaints = Complaint.objects.filter(status='PENDING').count()
        today_visitors = Visitor.objects.filter(arrival_time__date=timezone.now().date()).count()
        
        # Monthly Chart Data for 6 months
        labels = []
        income_data = []
        expense_data = []
        now = timezone.now().date()
        for i in range(5, -1, -1):
            year = now.year
            month = now.month - i
            while month <= 0:
                month += 12
                year -= 1
            month_start = datetime(year, month, 1).date()
            if month == 12:
                next_month_start = datetime(year + 1, 1, 1).date()
            else:
                next_month_start = datetime(year, month + 1, 1).date()
            
            labels.append(month_start.strftime("%B %Y"))
            inc = Transaction.objects.filter(transaction_type='INCOME', date__gte=month_start, date__lt=next_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
            exp = Transaction.objects.filter(transaction_type='EXPENSE', date__gte=month_start, date__lt=next_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
            income_data.append(float(inc))
            expense_data.append(float(exp))

        context.update({
            'total_collected': total_collected,
            'total_expenses': total_expenses,
            'unpaid_dues': unpaid_dues,
            'paid_dues': paid_dues,
            'net_cash': total_collected - total_expenses,
            'open_complaints': open_complaints,
            'today_visitors': today_visitors,
            'recent_tasks': Task.objects.all().order_by('-date_assigned')[:5],
            'chart_labels_json': json.dumps(labels),
            'chart_income_json': json.dumps(income_data),
            'chart_expense_json': json.dumps(expense_data),
            'chart_dues_status_json': json.dumps([float(paid_dues), float(unpaid_dues)]),
        })
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'

class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pets.html'
    context_object_name = 'pets'

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    template_name = 'pet_form.html'
    fields = ['pet_name', 'pet_type', 'notes']
    success_url = reverse_lazy('pets')
    
    def form_valid(self, form):
        form.instance.resident = self.request.user.resident
        return super().form_valid(form)

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers.html'
    context_object_name = 'suppliers'

class BulkDueCreateView(LoginRequiredMixin, StaffRequiredMixin, FormView):
    template_name = 'bulk_due_form.html'
    form_class = BulkDueForm
    success_url = reverse_lazy('dues')
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        issue_date = form.cleaned_data['issue_date']
        due_date = form.cleaned_data['due_date']
        
        residents = Resident.objects.all()
        for resident in residents:
            Due.objects.create(
                resident=resident,
                amount=amount,
                issue_date=issue_date,
                due_date=due_date,
                is_paid=False
            )
        messages.success(self.request, f"{residents.count()} adet daireye {amount} TL tutarında toplu aidat tanımlandı.")
        return super().form_valid(form)

class TransactionCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('transactions')

class TaskCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')

class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user.is_staff or (hasattr(request.user, 'resident') and task.staff == request.user.resident):
            status = request.POST.get('status')
            if status in ['PENDING', 'IN_PROGRESS', 'DONE']:
                task.status = status
                task.save()
        return redirect('tasks')

class ComplaintResolveView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = 'RESOLVED'
        complaint.save()
        messages.success(request, f"'{complaint.title}' konulu talep çözüldü olarak işaretlendi.")
        return redirect('complaints')

# ==================== 2. EL KOMŞU PAZARI (MARKETPLACE) ====================

class MarketplaceListView(LoginRequiredMixin, ListView):
    model = MarketplaceItem
    template_name = 'marketplace.html'
    context_object_name = 'items'

    def get_queryset(self):
        qs = MarketplaceItem.objects.all().select_related('resident')
        item_type = self.request.GET.get('type')
        q = self.request.GET.get('q')
        
        if item_type in ['FOR_SALE', 'FOR_RENT', 'FREE']:
            qs = qs.filter(item_type=item_type)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

class MarketplaceCreateView(LoginRequiredMixin, CreateView):
    model = MarketplaceItem
    form_class = MarketplaceItemForm
    template_name = 'marketplace_form.html'
    success_url = reverse_lazy('marketplace')

    def form_valid(self, form):
        if not hasattr(self.request.user, 'resident'):
            messages.error(self.request, "İlan oluşturmak için kayıtlı bir sakin hesabına sahip olmalısınız.")
            return redirect('marketplace')
        form.instance.resident = self.request.user.resident
        messages.success(self.request, "İlanınız başarıyla yayınlandı!")
        return super().form_valid(form)

class MarketplaceToggleSoldView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(MarketplaceItem, pk=pk)
        if request.user.is_staff or (hasattr(request.user, 'resident') and item.resident == request.user.resident):
            item.is_sold = not item.is_sold
            item.save()
            messages.info(request, "İlan durumu güncellendi.")
        return redirect('marketplace')

# ==================== ACİL DURUM & BİLDİRİMLER ====================

class EmergencyAlertListView(LoginRequiredMixin, ListView):
    model = EmergencyAlert
    template_name = 'emergency_alerts.html'
    context_object_name = 'alerts'

class EmergencyAlertCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = EmergencyAlert
    form_class = EmergencyAlertForm
    template_name = 'emergency_alert_form.html'
    success_url = reverse_lazy('emergency_alerts')

    def form_valid(self, form):
        messages.success(self.request, "Acil durum duyurusu tüm sakinlere yayınlandı!")
        return super().form_valid(form)

class EmergencyAlertToggleView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        alert = get_object_or_404(EmergencyAlert, pk=pk)
        alert.is_active = not alert.is_active
        alert.save()
        messages.info(request, f"Duyuru durumu {'aktif' if alert.is_active else 'pasif'} olarak güncellendi.")
        return redirect('emergency_alerts')

# ==================== SAKİN PROFİLİ & HESAP ====================

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        resident = getattr(request.user, 'resident', None)
        form = ResidentProfileForm(instance=resident) if resident else None
        
        my_vehicles = Vehicle.objects.filter(resident=resident) if resident else []
        my_pets = Pet.objects.filter(resident=resident) if resident else []
        my_bookings = Booking.objects.filter(resident=resident).order_by('-start_time')[:5] if resident else []
        my_dues = Due.objects.filter(resident=resident).order_by('-issue_date')[:5] if resident else []
        my_items = MarketplaceItem.objects.filter(resident=resident) if resident else []

        return render(request, 'profile.html', {
            'resident': resident,
            'form': form,
            'vehicles': my_vehicles,
            'pets': my_pets,
            'bookings': my_bookings,
            'dues': my_dues,
            'items': my_items,
        })

    def post(self, request):
        resident = getattr(request.user, 'resident', None)
        if not resident:
            messages.error(request, "Profil düzenleme yetkiniz yok.")
            return redirect('dashboard')
        
        form = ResidentProfileForm(request.POST, request.FILES, instance=resident)
        if form.is_valid():
            form.save()
            # Also update user email
            if resident.email:
                request.user.email = resident.email
                request.user.save()
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi.")
            return redirect('profile')
        
        return render(request, 'profile.html', {'resident': resident, 'form': form})

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Şifreniz başarıyla değiştirildi.")
        return super().form_valid(form)

# ==================== EXCEL / CSV DIŞA AKTARMA ====================

def export_dues_csv(request):
    if not request.user.is_staff:
        return HttpResponse("Yetkisiz erişim", status=403)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="aidat_listesi_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
    response.write(u'\ufeff'.encode('utf8')) # Excel UTF-8 BOM

    writer = csv.writer(response)
    writer.writerow(['Daire No', 'Sakin Adı Soyadı', 'Tutar (TL)', 'Kesim Tarihi', 'Son Ödeme Tarihi', 'Durum', 'Telefon', 'E-posta'])

    dues = Due.objects.all().select_related('resident').order_by('resident__flat_number', '-issue_date')
    for due in dues:
        writer.writerow([
            due.resident.flat_number,
            f"{due.resident.first_name} {due.resident.last_name}",
            due.amount,
            due.issue_date.strftime("%d.%m.%Y"),
            due.due_date.strftime("%d.%m.%Y"),
            "ÖDENDİ" if due.is_paid else "BEKLİYOR",
            due.resident.phone_number or "-",
            due.resident.email or "-"
        ])
    return response

def export_transactions_csv(request):
    if not request.user.is_staff:
        return HttpResponse("Yetkisiz erişim", status=403)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="kasa_hareketleri_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
    response.write(u'\ufeff'.encode('utf8')) # Excel UTF-8 BOM

    writer = csv.writer(response)
    writer.writerow(['Tarih', 'İşlem Tipi', 'Tutar (TL)', 'Açıklama'])

    transactions = Transaction.objects.all().order_by('-date')
    for tx in transactions:
        writer.writerow([
            tx.date.strftime("%d.%m.%Y"),
            tx.get_transaction_type_display(),
            tx.amount,
            tx.description
        ])
    return response
