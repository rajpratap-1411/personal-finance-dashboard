from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Sum, Q
from django.utils import timezone
from transactions.models import Transaction
import json
from datetime import datetime, timedelta
from calendar import month_name

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
        
        # Get recent transactions (last 5)
        context['recent_transactions'] = Transaction.objects.filter(
            user=user
        ).select_related('category').order_by('-date', '-created_at')[:5]
        
        # Get this month's total (already calculated in monthly_data)
        context['this_month_total'] = monthly_data['total_expenses']
        
        # Convert to JSON for charts
        context['chart_data'] = json.dumps({
            'monthly_trends': context['monthly_trends'],
            'category_expenses': context['category_expenses'],
            'category_income': context['category_income'],
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
            'savings_percentage': round((savings / income * 100) if income > 0 else 0, 2),
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
        trends = []
        now = timezone.now()
        
        for i in range(months_count - 1, -1, -1):
            # Calculate target month
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
                'month': f"{month_name[month][:3]} {year}",
                'income': float(income),
                'expenses': float(expenses),
                'savings': float(income - expenses),
            })
        
        return trends
