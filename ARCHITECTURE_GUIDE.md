# Personal Finance Dashboard - Architecture & Implementation Guide

## 📋 Table of Contents
1. [Database Schema (Models)](#database-schema-models)
2. [Application Structure](#application-structure)
3. [Business Logic & Methods](#business-logic--methods)
4. [Views & URL Routing](#views--url-routing)
5. [Charts & Visualization](#charts--visualization)
6. [Authentication & Security](#authentication--security)
7. [Budget Alerts System](#budget-alerts-system)

---

## 🗄️ Database Schema (Models)

### Core Models Structure

#### 1. **Category Model**
```python
# Purpose: Store income and expense categories
Fields:
- id (Primary Key, Auto)
- name (CharField, max_length=100)
- type (CharField: 'income' or 'expense')
- user (ForeignKey to User)
- created_at (DateTimeField)
- icon (CharField, optional - for UI)
```

#### 2. **Transaction Model** (Main Model)
```python
# Purpose: Store all financial transactions (income & expenses)
Fields:
- id (Primary Key, Auto)
- user (ForeignKey to User)
- type (CharField: 'income' or 'expense')
- category (ForeignKey to Category)
- amount (DecimalField, max_digits=10, decimal_places=2)
- description (TextField, optional)
- date (DateField)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)
```

#### 3. **Budget Model** (Optional - for Budget Alerts)
```python
# Purpose: Set monthly budgets for categories
Fields:
- id (Primary Key, Auto)
- user (ForeignKey to User)
- category (ForeignKey to Category)
- amount (DecimalField - budget limit)
- month (IntegerField, 1-12)
- year (IntegerField)
- created_at (DateTimeField)
```

#### 4. **User Profile Model** (Optional Extension)
```python
# Purpose: Store additional user information
Fields:
- user (OneToOneField to User)
- currency (CharField, default='USD')
- timezone (CharField)
- created_at (DateTimeField)
```

---

## 🏗️ Application Structure

### Recommended Django Apps:

```
personal-finance-dashboard/
├── manage.py
├── personal_finance_dashboard/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/              # User authentication & profiles
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── transactions/          # Core transaction management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
├── dashboard/             # Dashboard views & charts
│   ├── views.py
│   ├── utils.py          # Calculation helpers
│   └── urls.py
└── templates/
    ├── base.html
    ├── accounts/
    ├── transactions/
    └── dashboard/
```

---

## 💡 Business Logic & Methods

### 1. **Transaction Management Methods**

#### Add Transaction
```python
def add_transaction(user, type, category, amount, date, description=None):
    """
    Logic:
    1. Validate amount > 0
    2. Validate category belongs to user
    3. Validate category type matches transaction type
    4. Create transaction record
    5. Return success/error
    """
```

#### Update Transaction
```python
def update_transaction(transaction_id, user, **kwargs):
    """
    Logic:
    1. Verify transaction belongs to user
    2. Validate new data
    3. Update transaction
    4. Return updated transaction
    """
```

#### Delete Transaction
```python
def delete_transaction(transaction_id, user):
    """
    Logic:
    1. Verify ownership
    2. Delete transaction
    3. Return success
    """
```

### 2. **Financial Calculations**

#### Monthly Totals
```python
def get_monthly_totals(user, year, month):
    """
    Logic:
    1. Filter transactions by user, year, month
    2. Group by type (income/expense)
    3. Sum amounts for each type
    4. Calculate savings = income - expenses
    5. Return dict: {
        'income': total_income,
        'expenses': total_expenses,
        'savings': savings
    }
    """
```

#### Category-wise Totals
```python
def get_category_totals(user, year, month, transaction_type='expense'):
    """
    Logic:
    1. Filter transactions by user, year, month, type
    2. Group by category
    3. Sum amounts per category
    4. Return dict: {category_name: total_amount}
    """
```

#### Monthly Trends (for Charts)
```python
def get_monthly_trends(user, start_date, end_date):
    """
    Logic:
    1. Filter transactions in date range
    2. Group by month
    3. Calculate income/expense per month
    4. Return list: [
        {'month': '2024-01', 'income': 5000, 'expenses': 3000},
        ...
    ]
    """
```

### 3. **Budget Alert Logic**

#### Check Budget Alerts
```python
def check_budget_alerts(user, year, month):
    """
    Logic:
    1. Get all budgets for user, year, month
    2. Get actual expenses per category
    3. Compare actual vs budget
    4. Return alerts: [
        {
            'category': 'Food',
            'budget': 500,
            'spent': 600,
            'percentage': 120,
            'alert': 'exceeded'
        },
        ...
    ]
    """
```

#### Calculate Budget Percentage
```python
def get_budget_percentage(budget_amount, spent_amount):
    """
    Logic:
    1. Calculate percentage = (spent / budget) * 100
    2. Return percentage and status:
       - < 80%: 'safe'
       - 80-100%: 'warning'
       - > 100%: 'exceeded'
    """
```

---

## 🎨 Views & URL Routing

### View Types:

#### 1. **Class-Based Views (Recommended)**
```python
# Transaction Views
- TransactionListView (List all transactions)
- TransactionCreateView (Add new transaction)
- TransactionUpdateView (Edit transaction)
- TransactionDeleteView (Delete transaction)

# Dashboard Views
- DashboardView (Main dashboard with charts)
- MonthlyReportView (Monthly summary)
- CategoryReportView (Category breakdown)
```

#### 2. **Function-Based Views (Alternative)**
```python
# For simpler views or custom logic
- dashboard_view()
- add_transaction_view()
- transaction_list_view()
```

### URL Structure:
```python
# Main URLs (personal_finance_dashboard/urls.py)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
]

# Dashboard URLs
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('monthly-report/', MonthlyReportView.as_view(), name='monthly_report'),
]

# Transaction URLs
urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('add/', TransactionCreateView.as_view(), name='add_transaction'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='edit_transaction'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete_transaction'),
]

# Account URLs
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
```

---

## 📊 Charts & Visualization

### Chart Libraries (Choose One):

#### Option 1: Chart.js (Recommended - Client-side)
```javascript
// Advantages: Lightweight, no server processing
// Usage: Pass data as JSON to template, render in browser
```

#### Option 2: Plotly (Interactive)
```python
# Advantages: Highly interactive, professional charts
# Usage: Generate HTML in Django view, embed in template
```

#### Option 3: Matplotlib + Base64 (Server-side)
```python
# Advantages: Full Python control
# Usage: Generate image, convert to base64, embed in HTML
```

### Chart Types Needed:

1. **Monthly Income vs Expenses (Line/Bar Chart)**
   - X-axis: Months
   - Y-axis: Amount
   - Two lines/bars: Income & Expenses

2. **Category-wise Expenses (Pie/Doughnut Chart)**
   - Each slice = Category
   - Size = Percentage of total expenses

3. **Savings Trend (Line Chart)**
   - X-axis: Months
   - Y-axis: Savings amount
   - Shows savings over time

4. **Budget vs Actual (Bar Chart)**
   - X-axis: Categories
   - Two bars per category: Budget & Actual

### Data Preparation for Charts:
```python
def prepare_chart_data(user, year, month):
    """
    Returns JSON-ready data for charts:
    {
        'monthly_trends': [...],
        'category_expenses': {...},
        'income_vs_expense': {...},
        'savings_trend': [...]
    }
    """
```

---

## 🔐 Authentication & Security

### Authentication Flow:

1. **User Registration**
   - Create user account
   - Validate email (optional)
   - Set password (hashed by Django)

2. **User Login**
   - Authenticate credentials
   - Create session
   - Redirect to dashboard

3. **Session Management**
   - Django handles sessions automatically
   - Use `@login_required` decorator

### Security Best Practices:

```python
# Views should check user ownership
@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction.user != request.user:
        raise PermissionDenied
    # ... rest of view
```

### User Filtering:
```python
# Always filter by user in queries
transactions = Transaction.objects.filter(user=request.user)
```

---

## 🚨 Budget Alerts System

### Alert Types:

1. **Budget Exceeded**
   - When spent > budget
   - Show red alert

2. **Budget Warning**
   - When spent > 80% of budget
   - Show yellow warning

3. **Budget Safe**
   - When spent < 80% of budget
   - Show green status

### Implementation:

```python
# In Dashboard View
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    alerts = check_budget_alerts(
        self.request.user,
        current_year,
        current_month
    )
    context['budget_alerts'] = alerts
    return context
```

### Alert Display:
```html
<!-- In Template -->
{% for alert in budget_alerts %}
    <div class="alert alert-{{ alert.status }}">
        {{ alert.category }}: 
        Spent {{ alert.spent }} / Budget {{ alert.budget }}
        ({{ alert.percentage }}%)
    </div>
{% endfor %}
```

---

## 🔄 Data Flow Architecture

### Request Flow:
```
User Request
    ↓
URL Router
    ↓
View (Business Logic)
    ↓
Model (Database Query)
    ↓
Template (HTML + Data)
    ↓
Response (Rendered Page)
```

### Example: Adding a Transaction
```
1. User fills form → POST /transactions/add/
2. TransactionCreateView receives data
3. Form validation
4. Create Transaction object
5. Save to database
6. Redirect to transaction list
7. Show success message
```

---

## 📝 Key Methods Summary

### Model Methods:
- `Transaction.objects.filter(user=user, date__year=year, date__month=month)`
- `Transaction.objects.aggregate(Sum('amount'))`
- `Transaction.objects.values('category').annotate(total=Sum('amount'))`

### View Methods:
- `get_queryset()` - Filter data for current user
- `form_valid()` - Handle successful form submission
- `get_context_data()` - Add extra data to template

### Utility Functions:
- `calculate_monthly_totals()`
- `get_category_breakdown()`
- `check_budget_alerts()`
- `prepare_chart_data()`

---

## 🎯 Implementation Priority

### Phase 1: Core Functionality
1. Create Django apps (accounts, transactions, dashboard)
2. Define models (Category, Transaction)
3. Create basic views (CRUD for transactions)
4. Set up authentication

### Phase 2: Dashboard & Charts
1. Create dashboard view
2. Implement calculation methods
3. Add chart visualizations
4. Monthly and category reports

### Phase 3: Advanced Features
1. Budget model and management
2. Budget alert system
3. Advanced filtering and search
4. Export functionality (optional)

---

## 📚 Additional Considerations

### Performance:
- Use `select_related()` for ForeignKey queries
- Use `prefetch_related()` for ManyToMany queries
- Add database indexes on frequently queried fields
- Consider caching for dashboard calculations

### Testing:
- Unit tests for models
- View tests for CRUD operations
- Integration tests for calculations

### Future Enhancements:
- Recurring transactions
- Multiple currencies
- Financial goals tracking
- Export to CSV/PDF
- Mobile responsive design

---

This architecture provides a solid foundation for your Personal Finance Dashboard. Each component is modular and can be implemented incrementally.

