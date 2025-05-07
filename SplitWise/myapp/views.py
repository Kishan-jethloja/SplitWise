from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import ExpenseShare, Group, Expense, Settlement
from .forms import UserRegistrationForm, GroupForm, ExpenseForm, SettlementForm
from decimal import Decimal
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from django.db import transaction

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing_page.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # Create username from email (before @)
        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = email  # Use full email as username if split username exists

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def dashboard(request):
    user_groups = request.user.custom_groups.all()
    user_expenses = Expense.objects.filter(group__in=user_groups)
    total_owed = ExpenseShare.objects.filter(user=request.user).aggregate(total=models.Sum('amount_owed'))['total'] or 0
    total_paid = Expense.objects.filter(paid_by=request.user).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'groups': user_groups,
        'expenses': user_expenses,
        'total_owed': total_owed,
        'total_paid': total_paid,
        'net_balance': total_paid - total_owed
    }
    return render(request, 'dashboard.html', context)

@login_required
def group_list(request):
    groups = request.user.custom_groups.all()
    return render(request, "group_list.html", {"groups": groups})

@login_required
def create_group(request):
    if request.method == "POST":
        group_name = request.POST.get('group_name')
        group_description = request.POST.get('group_description')
        members_emails = request.POST.get('members', '').split(',')

        group = Group.objects.create(name=group_name, description=group_description)
        group.members.add(request.user)

        for email in members_emails:
            email = email.strip()
            if email:
                try:
                    user = User.objects.get(email=email)
                    group.members.add(user)
                except User.DoesNotExist:
                    messages.warning(request, f"User with email {email} not found.")

        messages.success(request, "Group created successfully!")
        return redirect('group_list')

    return render(request, 'create_group.html')

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, "You don't have access to this group.")
        return redirect('group_list')
    
    expenses = group.expenses.all().order_by('-date')
    members = group.members.all()
    
    # Calculate balances for each member
    balances = {}
    for member in members:
        # Calculate expenses paid
        paid = sum(expense.amount for expense in expenses if expense.paid_by == member)
        
        # Calculate expenses owed
        owed = sum(share.amount_owed for expense in expenses for share in expense.shares.filter(user=member))
        
        # Calculate settlements made (positive for money paid)
        settlements_made = sum(settlement.amount for settlement in group.settlements.filter(payer=member))
        
        # Calculate settlements received (negative for money received)
        settlements_received = sum(settlement.amount for settlement in group.settlements.filter(payee=member))
        
        # Calculate final balance including settlements
        final_balance = paid - owed + settlements_made - settlements_received
        balances[member] = final_balance
    
    context = {
        'group': group,
        'expenses': expenses,
        'members': members,
        'balances': balances,
        'settlements': group.settlements.all().order_by('-date')  # Add settlements to context
    }
    return render(request, 'group_details.html', context)

@login_required
def expenses(request):
    # Get all groups the user is a member of
    user_groups = Group.objects.filter(members=request.user)
    
    # Base queryset for expenses
    expenses = Expense.objects.filter(
        Q(group__in=user_groups)
    ).select_related('group', 'paid_by').prefetch_related('shares').order_by('-date')
    
    # Apply filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    group_id = request.GET.get('group')
    expense_type = request.GET.get('type')
    
    if start_date:
        expenses = expenses.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        expenses = expenses.filter(date__lte=datetime.strptime(end_date, '%Y-%m-%d'))
    if group_id:
        expenses = expenses.filter(group_id=group_id)
    if expense_type == 'paid':
        expenses = expenses.filter(paid_by=request.user)
    elif expense_type == 'owed':
        expenses = expenses.filter(shares__user=request.user).exclude(paid_by=request.user)
    
    context = {
        'expenses': expenses,
        'groups': user_groups,
    }
    return render(request, 'expenses.html', context)

@login_required
def add_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, "You don't have access to this group.")
        return redirect('group_list')

    if request.method == "POST":
        description = request.POST.get('description')
        amount = Decimal(request.POST.get('amount'))
        split_type = request.POST.get('split_type')
        
        expense = Expense.objects.create(
            group=group,
            description=description,
            amount=amount,
            paid_by=request.user,
            split_type=split_type
        )

        members = group.members.all()
        if split_type == 'equal':
            split_amount = amount / members.count()
            for member in members:
                ExpenseShare.objects.create(
                    expense=expense,
                    user=member,
                    amount_owed=split_amount
                )
        else:  # percentage split
            for member in members:
                percentage = Decimal(request.POST.get(f'percentage_{member.id}', 0))
                amount_owed = (percentage / 100) * amount
                ExpenseShare.objects.create(
                    expense=expense,
                    user=member,
                    amount_owed=amount_owed
                )

        messages.success(request, "Expense added successfully!")
        return redirect('group_detail', group_id=group_id)

    context = {
        'group': group,
        'members': group.members.all()
    }
    return render(request, 'add_expense.html', context)

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, "You don't have access to this group.")
        return redirect('group_list')

    if request.method == "POST":
        group.name = request.POST.get('group_name')
        group.description = request.POST.get('group_description')
        group.save()
        messages.success(request, "Group updated successfully!")
        return redirect('group_detail', group_id=group.id)

    return redirect('group_detail', group_id=group.id)

@login_required
def add_group_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, "You don't have access to this group.")
        return redirect('group_list')

    if request.method == "POST":
        email = request.POST.get('member_email')
        try:
            user = User.objects.get(email=email)
            if user in group.members.all():
                messages.warning(request, f"{user.username} is already a member of this group.")
            else:
                group.members.add(user)
                messages.success(request, f"{user.username} has been added to the group!")
        except User.DoesNotExist:
            messages.error(request, f"No user found with email {email}")

    return redirect('group_detail', group_id=group.id)

@login_required
def delete_expense(request, group_id, expense_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        group = get_object_or_404(Group, id=group_id)
        expense = get_object_or_404(Expense, id=expense_id, group=group)
        
        # Check if user is in the group
        if request.user not in group.members.all():
            return JsonResponse({'error': 'You do not have access to this group'}, status=403)

        # Check if user is the one who paid
        if request.user != expense.paid_by:
            return JsonResponse({'error': 'Only the person who paid can delete this expense'}, status=403)

        # Delete the expense and its associated shares
        expense.delete()
        
        return JsonResponse({'success': True, 'message': 'Expense deleted successfully'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def settle_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return JsonResponse({'error': "You don't have access to this group."}, status=403)

    if request.method == "POST":
        try:
            payer = get_object_or_404(User, id=request.POST.get('payer'))
            payee = get_object_or_404(User, id=request.POST.get('payee'))
            amount = Decimal(request.POST.get('settlement_amount'))

            if payer == payee:
                return JsonResponse({'error': "Payer and payee cannot be the same person."}, status=400)

            # Create the settlement record
            settlement = Settlement.objects.create(
                group=group,
                payer=payer,
                payee=payee,
                amount=amount,
                date=timezone.now()
            )

            # Calculate new balances
            payer_balance = Expense.objects.filter(group=group, paid_by=payer).aggregate(total=models.Sum('amount'))['total'] or 0
            payee_balance = Expense.objects.filter(group=group, paid_by=payee).aggregate(total=models.Sum('amount'))['total'] or 0
            
            payer_owed = ExpenseShare.objects.filter(expense__group=group, user=payer).aggregate(total=models.Sum('amount_owed'))['total'] or 0
            payee_owed = ExpenseShare.objects.filter(expense__group=group, user=payee).aggregate(total=models.Sum('amount_owed'))['total'] or 0
            
            # Add settlement amounts to balances
            payer_balance += amount
            payee_balance -= amount

            return JsonResponse({
                'success': True,
                'message': f"Settlement of ₹{amount} recorded successfully!",
                'settlement': {
                    'id': settlement.id,
                    'amount': str(amount),
                    'payer': {
                        'id': payer.id,
                        'username': payer.username,
                        'new_balance': str(payer_balance - payer_owed)
                    },
                    'payee': {
                        'id': payee.id,
                        'username': payee.username,
                        'new_balance': str(payee_balance - payee_owed)
                    }
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)