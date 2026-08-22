from django import forms
from .models import Due, Transaction, Task, Booking, Visitor

class BulkDueForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Aidat Tutarı (TL)")
    issue_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Kesim Tarihi")
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Son Ödeme Tarihi")

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'receipt']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['staff', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.facility = kwargs.pop('facility', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Başlangıç zamanı bitiş zamanından sonra veya aynı olamaz.")

            # Çakışma kontrolü
            overlaps = Booking.objects.filter(
                facility=self.facility,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance and self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                raise forms.ValidationError("Bu zaman aralığında tesiste başka bir rezervasyon zaten mevcut.")
        return cleaned_data

from .models import MarketplaceItem, EmergencyAlert, Resident

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['title', 'item_type', 'price', 'description', 'image', 'contact_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ürün veya eşyanın detaylarını, durumunu yazınız...'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Örn: 250 (Ücretsizse boş bırakın)'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Örn: 0555 123 4567'}),
        }

class EmergencyAlertForm(forms.ModelForm):
    class Meta:
        model = EmergencyAlert
        fields = ['title', 'severity', 'message', 'is_active']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Kesinti veya uyarı detaylarını yazınız...'}),
        }

class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['phone_number', 'email', 'profile_picture']

