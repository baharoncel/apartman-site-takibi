from django.contrib import admin
from .models import (
    Resident, Due, Transaction, Notice, Complaint, Vehicle, Poll, Choice, 
    Facility, Booking, Visitor, Staff, Inventory, Document, MessageBoard, 
    Task, Pet, Supplier, MarketplaceItem, EmergencyAlert
)

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'flat_number', 'phone_number')
    search_fields = ('first_name', 'last_name', 'flat_number')

@admin.register(Due)
class DueAdmin(admin.ModelAdmin):
    list_display = ('resident', 'amount', 'issue_date', 'due_date', 'is_paid')
    list_filter = ('is_paid', 'issue_date')
    search_fields = ('resident__first_name', 'resident__last_name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'date', 'description')
    list_filter = ('transaction_type', 'date')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('resident', 'title', 'status', 'date_submitted')
    list_filter = ('status', 'date_submitted')
    search_fields = ('title', 'resident__first_name', 'resident__last_name')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand_model', 'color', 'resident')
    search_fields = ('license_plate', 'resident__first_name', 'resident__last_name')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    exclude = ('votes',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'end_date', 'is_active')
    inlines = [ChoiceInline]

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('facility', 'resident', 'start_time', 'end_time')
    list_filter = ('facility', 'start_time')

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'visitor_type', 'resident', 'arrival_time')
    list_filter = ('visitor_type', 'arrival_time')
    search_fields = ('visitor_name', 'resident__first_name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'phone', 'salary')
    search_fields = ('first_name', 'last_name', 'role')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'location', 'purchase_date', 'warranty_end')
    search_fields = ('item_name', 'location')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    search_fields = ('title',)

@admin.register(MessageBoard)
class MessageBoardAdmin(admin.ModelAdmin):
    list_display = ('resident', 'content', 'timestamp')
    search_fields = ('resident__first_name', 'content')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'staff', 'status', 'date_assigned')
    list_filter = ('status', 'date_assigned')
    search_fields = ('title', 'staff__first_name')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'pet_type', 'resident')
    search_fields = ('pet_name', 'pet_type', 'resident__first_name')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'category', 'phone')
    search_fields = ('company_name', 'category')

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'resident', 'item_type', 'price', 'is_sold', 'created_at')
    list_filter = ('item_type', 'is_sold', 'created_at')
    search_fields = ('title', 'description', 'resident__first_name')

@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'is_active', 'created_at')
    list_filter = ('severity', 'is_active')
    search_fields = ('title', 'message')

