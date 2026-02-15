# Quick Implementation Reference

## Step-by-Step Implementation Guide

### Step 1: Create Django Apps

```bash
python manage.py startapp accounts
python manage.py startapp transactions
python manage.py startapp dashboard
```

### Step 2: Update settings.py

Add apps to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'transactions',
    'dashboard',
]
```

Add login URLs:
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
```

---

## Models Implementation

### transactions/models.py

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['user', 'name', 'type']
        indexes = [
            models.Index(fields=['user', 'type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type', 'date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.type.title()}: {self.amount} - {self.category.name} ({self.date})"


class Budget(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'category', 'month', 'year']
        indexes = [
            models.Index(fields=['user', 'year', 'month']),
        ]
    
    def __str__(self):
        return f"Budget: {self.category.name} - {self.amount} ({self.month}/{self.year})"
```

---

## Views Implementation

### transactions/views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction, Category
from .forms import TransactionForm

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by type if provided
        transaction_type = self.request.GET.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by month/year if provided
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        if month and year:
            queryset = queryset.filter(date__year=year, date__month=month)
        
        return queryset.select_related('category')


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Transaction added successfully!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transaction_list')
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Transaction updated successfully!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction_list')
    template_name = 'transactions/confirm_delete.html'
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Transaction deleted successfully!')
        return super().delete(request, *args, **kwargs)
```

### dashboard/views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Sum, Q
from django.utils import timezone
from transactions.models import Transaction, Budget
import json

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get current month/year
        now = timezone.now()
        current_year = now.year
        current_month = now.month
        
        # Get monthly totals
        monthly_data = self.get_monthly_totals(user, current_year, current_month)
        context.update(monthly_data)
        
        # Get category breakdown
        context['category_expenses'] = self.get_category_totals(
            user, current_year, current_month, 'expense'
        )
        context['category_income'] = self.get_category_totals(
            user, current_year, current_month, 'income'
        )
        
        # Get monthly trends (last 6 months)
        context['monthly_trends'] = self.get_monthly_trends(user, 6)
        
        # Get budget alerts
        context['budget_alerts'] = self.check_budget_alerts(
            user, current_year, current_month
        )
        
        # Convert to JSON for charts
        context['chart_data'] = json.dumps({
            'monthly_trends': context['monthly_trends'],
            'category_expenses': context['category_expenses'],
        })
        
        return context
    
    def get_monthly_totals(self, user, year, month):
        """Calculate monthly income, expenses, and savings"""
        income = Transaction.objects.filter(
            user=user,
            type='income',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = Transaction.objects.filter(
            user=user,
            type='expense',
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        savings = income - expenses
        
        return {
            'total_income': income,
            'total_expenses': expenses,
            'savings': savings,
            'savings_percentage': (savings / income * 100) if income > 0 else 0,
        }
    
    def get_category_totals(self, user, year, month, transaction_type):
        """Get totals grouped by category"""
        totals = Transaction.objects.filter(
            user=user,
            type=transaction_type,
            date__year=year,
            date__month=month
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return {item['category__name']: float(item['total']) for item in totals}
    
    def get_monthly_trends(self, user, months_count=6):
        """Get trends for last N months"""
        from datetime import datetime, timedelta
        from calendar import month_name
        
        trends = []
        now = timezone.now()
        
        for i in range(months_count - 1, -1, -1):
            target_date = now - timedelta(days=30 * i)
            year = target_date.year
            month = target_date.month
            
            income = Transaction.objects.filter(
                user=user,
                type='income',
                date__year=year,
                date__month=month
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            expenses = Transaction.objects.filter(
                user=user,
                type='expense',
                date__year=year,
                date__month=month
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            trends.append({
                'month': f"{month_name[month]} {year}",
                'income': float(income),
                'expenses': float(expenses),
                'savings': float(income - expenses),
            })
        
        return trends
    
    def check_budget_alerts(self, user, year, month):
        """Check if budgets are exceeded"""
        alerts = []
        budgets = Budget.objects.filter(
            user=user,
            year=year,
            month=month
        ).select_related('category')
        
        for budget in budgets:
            actual = Transaction.objects.filter(
                user=user,
                category=budget.category,
                type='expense',
                date__year=year,
                date__month=month
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            percentage = (actual / budget.amount * 100) if budget.amount > 0 else 0
            
            if percentage > 100:
                status = 'exceeded'
            elif percentage > 80:
                status = 'warning'
            else:
                status = 'safe'
            
            alerts.append({
                'category': budget.category.name,
                'budget': float(budget.amount),
                'spent': float(actual),
                'percentage': round(percentage, 2),
                'status': status,
            })
        
        return alerts
```

---

## Forms Implementation

### transactions/forms.py

```python
from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'description', 'date']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter categories by user
            self.fields['category'].queryset = Category.objects.filter(user=user)
            
            # Filter by transaction type if type is selected
            if 'type' in self.data:
                transaction_type = self.data.get('type')
                self.fields['category'].queryset = Category.objects.filter(
                    user=user,
                    type=transaction_type
                )
```

---

## URL Configuration

### transactions/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='edit_transaction'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
]
```

### dashboard/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]
```

### accounts/urls.py

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
```

### personal_finance_dashboard/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
]
```

---

## Admin Configuration

### transactions/admin.py

```python
from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'category', 'amount', 'date', 'user', 'created_at']
    list_filter = ['type', 'date', 'created_at']
    search_fields = ['description', 'category__name', 'user__username']
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'month', 'year', 'user']
    list_filter = ['year', 'month']
    search_fields = ['category__name', 'user__username']
```

---

## Template Example (Base)

### templates/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Personal Finance Dashboard{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard' %}">Finance Dashboard</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
                    <a class="nav-link" href="{% url 'transaction_list' %}">Transactions</a>
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Chart.js Example

### templates/dashboard/index.html

```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="row mb-4">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5>Total Income</h5>
                <h2>${{ total_income|floatformat:2 }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5>Total Expenses</h5>
                <h2>${{ total_expenses|floatformat:2 }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5>Savings</h5>
                <h2>${{ savings|floatformat:2 }}</h2>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <canvas id="monthlyTrendChart"></canvas>
    </div>
    <div class="col-md-6">
        <canvas id="categoryChart"></canvas>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const chartData = {{ chart_data|safe }};
    
    // Monthly Trends Chart
    const monthlyCtx = document.getElementById('monthlyTrendChart').getContext('2d');
    new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: chartData.monthly_trends.map(t => t.month),
            datasets: [{
                label: 'Income',
                data: chartData.monthly_trends.map(t => t.income),
                borderColor: 'rgb(75, 192, 192)',
            }, {
                label: 'Expenses',
                data: chartData.monthly_trends.map(t => t.expenses),
                borderColor: 'rgb(255, 99, 132)',
            }]
        }
    });
    
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(chartData.category_expenses),
            datasets: [{
                data: Object.values(chartData.category_expenses),
            }]
        }
    });
</script>
{% endblock %}
```

---

## Running Migrations

```bash
# Create migrations
python manage.py makemigrations transactions

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

This reference provides ready-to-use code snippets for implementing your Personal Finance Dashboard!

