from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
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
        
        return queryset.select_related('category').order_by('-date', '-created_at')


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Transaction added successfully! ✅')
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
        messages.success(self.request, 'Transaction updated successfully! ✅')
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
        messages.success(request, 'Transaction deleted successfully! ✅')
        return super().delete(request, *args, **kwargs)


@login_required
def get_categories(request):
    """API endpoint to get categories based on type"""
    transaction_type = request.GET.get('type')
    if transaction_type:
        categories = Category.objects.filter(
            user=request.user,
            type=transaction_type
        ).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)
