from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/add_member/', views.add_group_member, name='add_group_member'),
    path('groups/<int:group_id>/add_expense/', views.add_expense, name='add_expense'),
    path('groups/<int:group_id>/expenses/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('groups/<int:group_id>/settle/', views.settle_expense, name='settle_expense'),
    path('expenses/', views.expenses, name='expenses'),
]
