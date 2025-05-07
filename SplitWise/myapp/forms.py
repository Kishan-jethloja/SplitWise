from django import forms
from django.contrib.auth.models import User
from .models import Group, Expense, Settlement

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Group
        fields = ["name", "description", "members"]

        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['group', 'description', 'amount', 'paid_by','split_type']

class SettlementForm(forms.ModelForm):
    class Meta:
        model = Settlement
        fields = ['payer', 'payee', 'group', 'amount']
