from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Group, Expense, ExpenseShare, Settlement

class ExpenseShareInline(admin.TabularInline):
    model = ExpenseShare
    extra = 1
    readonly_fields = ('amount_owed',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_count', 'member_list')
    search_fields = ('name', 'description')
    filter_horizontal = ('members',)
    list_filter = ('members',)
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Number of Members'
    
    def member_list(self, obj):
        members = obj.members.all()
        return format_html(', '.join([f'ID: {m.id} ({m.username})' for m in members]))
    member_list.short_description = 'Group Members'

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'formatted_amount', 'paid_by', 'group', 'date', 'split_type')
    list_filter = ('group', 'split_type', 'date', 'paid_by')
    search_fields = ('description', 'paid_by__username', 'group__name')
    date_hierarchy = 'date'
    inlines = [ExpenseShareInline]
    readonly_fields = ('date',)
    list_per_page = 20
    
    def formatted_amount(self, obj):
        return format_html('\u20B9{}', '{:.2f}'.format(obj.amount))
    formatted_amount.short_description = 'Amount'

    actions = ['mark_as_equal_split']
    
    @admin.action(description='Set selected expenses to equal split')
    def mark_as_equal_split(self, request, queryset):
        queryset.update(split_type='equal')

@admin.register(ExpenseShare)
class ExpenseShareAdmin(admin.ModelAdmin):
    list_display = ('expense', 'user', 'formatted_amount_owed', 'expense_date', 'expense_group')
    list_filter = ('user', 'expense__group', 'expense__date')
    search_fields = ('user__username', 'expense__description')
    readonly_fields = ('expense_date', 'expense_group')
    
    def formatted_amount_owed(self, obj):
        return format_html('\u20B9{}', '{:.2f}'.format(obj.amount_owed))
    formatted_amount_owed.short_description = 'Amount Owed'
    
    def expense_date(self, obj):
        return obj.expense.date
    expense_date.short_description = 'Date'
    
    def expense_group(self, obj):
        return obj.expense.group
    expense_group.short_description = 'Group'

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('payer', 'payee', 'group', 'formatted_amount', 'date', 'status_label')
    list_filter = ('group', 'date', 'payer', 'payee')
    search_fields = ('payer__username', 'payee__username', 'group__name')
    date_hierarchy = 'date'
    readonly_fields = ('date',)
    
    def formatted_amount(self, obj):
        return format_html('\u20B9{}', '{:.2f}'.format(obj.amount))
    formatted_amount.short_description = 'Amount'
    
    def status_label(self, obj):
        if obj.amount > 1000:
            return format_html('<span style="color: red; font-weight: bold">High Amount</span>')
        return format_html('<span style="color: green">Normal</span>')
    status_label.short_description = 'Status'

    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }
