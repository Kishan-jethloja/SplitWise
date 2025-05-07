from django import template
from decimal import Decimal
from django.db.models import Sum

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if not dictionary:
        return 0
    return dictionary.get(key, 0)

@register.filter(name='percentage')
def percentage(amount_owed, total_amount):
    if not total_amount:
        return 0
    return (Decimal(amount_owed) / Decimal(total_amount)) * 100

@register.filter(name='sum_amount')
def sum_amount(expenses):
    if not expenses:
        return 0
    return expenses.aggregate(total=Sum('amount'))['total'] or 0 