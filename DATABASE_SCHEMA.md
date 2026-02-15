# Database Schema - Visual Representation

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │ (Django Built-in)
│  (from auth)    │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴─────────────────────────────────────┐
    │                                           │
    │                                           │
┌───▼──────────┐                    ┌──────────▼──────┐
│  Category    │                    │   Transaction   │
├──────────────┤                    ├─────────────────┤
│ id (PK)      │                    │ id (PK)         │
│ user (FK)    │◄───────────────────┤ user (FK)       │
│ name         │      N:1           │ category (FK)   │
│ type         │                    │ type            │
│ icon         │                    │ amount          │
│ created_at   │                    │ description     │
└──────────────┘                    │ date            │
                                    │ created_at      │
                                    │ updated_at      │
                                    └─────────────────┘
                                             │
                                             │
                                    ┌────────▼──────────┐
                                    │      Budget       │
                                    ├───────────────────┤
                                    │ id (PK)           │
                                    │ user (FK)         │
                                    │ category (FK)     │
                                    │ amount            │
                                    │ month             │
                                    │ year              │
                                    │ created_at        │
                                    └───────────────────┘
```

## Detailed Field Specifications

### 1. Category Model
```python
Category
├── id: BigAutoField (Primary Key)
├── user: ForeignKey(User, on_delete=CASCADE)
├── name: CharField(max_length=100)
├── type: CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
├── icon: CharField(max_length=50, blank=True, null=True)  # e.g., 'food', 'salary'
└── created_at: DateTimeField(auto_now_add=True)

Indexes:
- (user, type)  # For faster filtering
- (user, name)  # For unique category names per user
```

### 2. Transaction Model
```python
Transaction
├── id: BigAutoField (Primary Key)
├── user: ForeignKey(User, on_delete=CASCADE)
├── category: ForeignKey(Category, on_delete=PROTECT)
├── type: CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
├── amount: DecimalField(max_digits=10, decimal_places=2)
├── description: TextField(blank=True, null=True)
├── date: DateField()
├── created_at: DateTimeField(auto_now_add=True)
└── updated_at: DateTimeField(auto_now=True)

Indexes:
- (user, date)  # For monthly/yearly queries
- (user, type, date)  # For filtered queries
- (user, category)  # For category-wise reports
```

### 3. Budget Model
```python
Budget
├── id: BigAutoField (Primary Key)
├── user: ForeignKey(User, on_delete=CASCADE)
├── category: ForeignKey(Category, on_delete=CASCADE)
├── amount: DecimalField(max_digits=10, decimal_places=2)
├── month: IntegerField(choices=[(1, 'January'), ..., (12, 'December')])
├── year: IntegerField()
└── created_at: DateTimeField(auto_now_add=True)

Unique Constraint:
- (user, category, month, year)  # One budget per category per month

Indexes:
- (user, year, month)  # For monthly budget queries
```

## Sample Data Examples

### Categories
```
id | user_id | name      | type    | icon
---|---------|-----------|---------|--------
1  | 1       | Salary    | income  | salary
2  | 1       | Freelance | income  | work
3  | 1       | Food      | expense | food
4  | 1       | Transport | expense | car
5  | 1       | Rent      | expense | home
```

### Transactions
```
id | user_id | category_id | type    | amount  | date       | description
---|---------|-------------|---------|---------|------------|------------
1  | 1       | 1           | income  | 5000.00 | 2024-01-01 | Monthly salary
2  | 1       | 3           | expense | 150.00  | 2024-01-02 | Groceries
3  | 1       | 4           | expense | 50.00   | 2024-01-03 | Gas
4  | 1       | 5           | expense | 1200.00 | 2024-01-05 | Rent payment
```

### Budgets
```
id | user_id | category_id | amount  | month | year
---|---------|-------------|---------|-------|------
1  | 1       | 3           | 500.00  | 1     | 2024
2  | 1       | 4           | 200.00  | 1     | 2024
3  | 1       | 5           | 1200.00 | 1     | 2024
```

## Query Patterns

### Common Queries:

1. **Get all transactions for a user in a month:**
```python
Transaction.objects.filter(
    user=user,
    date__year=2024,
    date__month=1
)
```

2. **Get monthly totals:**
```python
from django.db.models import Sum, Q

income = Transaction.objects.filter(
    user=user,
    type='income',
    date__year=2024,
    date__month=1
).aggregate(total=Sum('amount'))['total'] or 0

expenses = Transaction.objects.filter(
    user=user,
    type='expense',
    date__year=2024,
    date__month=1
).aggregate(total=Sum('amount'))['total'] or 0
```

3. **Get category-wise totals:**
```python
from django.db.models import Sum

Transaction.objects.filter(
    user=user,
    type='expense',
    date__year=2024,
    date__month=1
).values('category__name').annotate(
    total=Sum('amount')
).order_by('-total')
```

4. **Get budget vs actual:**
```python
from django.db.models import Sum, F

budgets = Budget.objects.filter(
    user=user,
    year=2024,
    month=1
).select_related('category')

for budget in budgets:
    actual = Transaction.objects.filter(
        user=user,
        category=budget.category,
        type='expense',
        date__year=2024,
        date__month=1
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    percentage = (actual / budget.amount) * 100 if budget.amount > 0 else 0
```

## Database Relationships

### Foreign Key Relationships:
- **User → Category**: One user can have many categories
- **User → Transaction**: One user can have many transactions
- **User → Budget**: One user can have many budgets
- **Category → Transaction**: One category can have many transactions
- **Category → Budget**: One category can have many budgets (different months)

### Cascade Behaviors:
- **CASCADE**: When user is deleted, delete all their categories, transactions, and budgets
- **PROTECT**: Cannot delete a category if it has transactions (prevents data loss)

## Migration Strategy

### Initial Migration Order:
1. Create Category model
2. Create Transaction model (depends on Category)
3. Create Budget model (depends on Category)

### Future Migrations:
- Add indexes for performance
- Add constraints (unique, check)
- Add new fields as features expand

