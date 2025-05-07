from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="custom_groups")  

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        ordering = ['name']

class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses", db_index=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid", db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    split_type = models.CharField(
        max_length=20, 
        choices=[("equal", "Equal"), ("percentage", "Percentage")], 
        default="equal",
        db_index=True
    )

    def __str__(self):
        return f"{self.description} - {self.amount}"

    class Meta:
        indexes = [
            models.Index(fields=['date', 'group']),
            models.Index(fields=['paid_by', 'group']),
            models.Index(fields=['amount', 'split_type']),
        ]
        ordering = ['-date']

class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="shares", db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense_shares", db_index=True)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    def __str__(self):
        return f"{self.user.username} owes {self.amount_owed} for {self.expense.description}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'expense']),
            models.Index(fields=['amount_owed']),
        ]
        unique_together = ['expense', 'user']
        ordering = ['-expense__date', 'user__username']

class Settlement(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_made", db_index=True)
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_received", db_index=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="settlements", db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.payer.username} paid {self.amount} to {self.payee.username}"

    class Meta:
        indexes = [
            models.Index(fields=['date', 'group']),
            models.Index(fields=['payer', 'payee']),
            models.Index(fields=['amount']),
        ]
        ordering = ['-date']
