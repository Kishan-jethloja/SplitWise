# Generated by Django 5.1.3 on 2025-03-04 16:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_paid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_owed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='myapp.expense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_shares', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('members', models.ManyToManyField(related_name='custom_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='myapp.group'),
        ),
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settlements', to='myapp.group')),
                ('payee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settlements_received', to=settings.AUTH_USER_MODEL)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settlements_made', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
