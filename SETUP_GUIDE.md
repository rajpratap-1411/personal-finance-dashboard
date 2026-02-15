# 🚀 Personal Finance Dashboard - Setup Guide

## ✅ Project Complete! Ab Kaise Use Kare?

### Step 1: Virtual Environment Activate Kare
```powershell
cd C:\Users\rajpr\Downloads\personal-finance-dashboard
.\venv\Scripts\Activate.ps1
```

### Step 2: Server Start Kare
```powershell
python manage.py runserver
```

### Step 3: Browser Mein Kholo
```
http://127.0.0.1:8000
```

---

## 📝 Pehli Baar Use Karne Ke Liye

### 1. **Superuser Banao** (Admin Panel ke liye)
```powershell
python manage.py createsuperuser
```
- Username, email, password enter karein
- Admin panel: `http://127.0.0.1:8000/admin`

### 2. **User Register Karein**
- Browser mein `http://127.0.0.1:8000/accounts/register` kholo
- Username aur password se register karein
- **Automatic:** Default categories create ho jayengi (Food, Rent, Salary, etc.)

### 3. **Login Karein**
- `http://127.0.0.1:8000/accounts/login`
- Username aur password se login karein

---

## 💰 Kaise Use Kare?

### **Income Add Karne Ke Liye:**
1. Dashboard se "Add Transaction" click karein
2. Type: **Income** select karein
3. Category: Salary/Freelance/Investment select karein
4. Amount: ₹50,000 enter karein
5. Date: Select karein
6. Save karein

### **Expense Add Karne Ke Liye:**
1. Dashboard se "Add Transaction" click karein
2. Type: **Expense** select karein
3. Category: Food/Transport/Rent select karein
4. Amount: ₹8,000 enter karein
5. Date: Select karein
6. Save karein

### **Dashboard Dekhne Ke Liye:**
- Login ke baad automatically dashboard dikhega
- Yahan dikhega:
  - ✅ Total Income
  - ✅ Total Expense
  - ✅ Savings (Income - Expense)
  - ✅ Category-wise Chart (Pie Chart)
  - ✅ Monthly Trend (Line Chart)

---

## 🎯 Features

### ✅ **Working Features:**
1. **User Authentication** - Login/Register/Logout
2. **Add Income** - Salary, Freelance, etc.
3. **Add Expense** - Food, Rent, Transport, etc.
4. **View Transactions** - List of all transactions
5. **Edit/Delete** - Transactions ko edit ya delete kar sakte hain
6. **Dashboard** - Real-time calculations
7. **Charts** - Category-wise aur Monthly trends
8. **Auto Categories** - New user ke liye default categories

### 📊 **Dashboard Shows:**
- Total Income (Green card)
- Total Expense (Red card)
- Savings (Purple card)
- Expense by Category (Pie Chart)
- Monthly Income vs Expense Trend (Line Chart)
- Category Breakdown (List)

---

## 🗂️ Default Categories

### Income Categories:
- Salary
- Freelance
- Investment
- Other Income

### Expense Categories:
- Food
- Transport
- Rent
- Utilities
- Shopping
- Entertainment
- Healthcare
- Education
- Other Expense

**Note:** Agar category nahi mil rahi, to Admin panel se add kar sakte hain.

---

## 🔧 Admin Panel

### Categories Add Karne Ke Liye:
1. `http://127.0.0.1:8000/admin` kholo
2. Login karein (superuser se)
3. Transactions → Categories
4. "Add Category" click karein
5. Name, Type (Income/Expense), User select karein
6. Save karein

---

## 📱 URLs

- **Dashboard:** `http://127.0.0.1:8000/`
- **Login:** `http://127.0.0.1:8000/accounts/login`
- **Register:** `http://127.0.0.1:8000/accounts/register`
- **Transactions:** `http://127.0.0.1:8000/transactions/`
- **Add Transaction:** `http://127.0.0.1:8000/transactions/add/`
- **Admin:** `http://127.0.0.1:8000/admin`

---

## 🎨 UI Features

- **Modern Design** - Bootstrap 5 with gradients
- **Responsive** - Mobile aur desktop dono pe kaam karta hai
- **Charts** - Chart.js se beautiful visualizations
- **Color Coding:**
  - 🟢 Green = Income
  - 🔴 Red = Expense
  - 🟣 Purple = Savings

---

## 🐛 Troubleshooting

### Problem: Categories nahi dikh rahi
**Solution:** Admin panel se manually add karein ya management command run karein:
```powershell
python manage.py create_default_categories <username>
```

### Problem: Database error
**Solution:** Migrations run karein:
```powershell
python manage.py migrate
```

### Problem: Charts nahi dikh rahe
**Solution:** Internet connection check karein (Chart.js CDN se load hota hai)

---

## ✅ Project Status: **COMPLETE & WORKING!**

Ab aap:
1. ✅ Income add kar sakte hain
2. ✅ Expense add kar sakte hain
3. ✅ Dashboard mein sab kuch dekh sakte hain
4. ✅ Charts dekh sakte hain
5. ✅ Transactions edit/delete kar sakte hain

**Happy Tracking! 💰📊**

