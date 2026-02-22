from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'description', 'date']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition outline-none',
                'id': 'id_type',
                'onchange': 'updateCategories()'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition outline-none',
                'id': 'id_category'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition outline-none',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition outline-none resize-none',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition outline-none',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Initially show all categories, will be filtered by JavaScript
            self.fields['category'].queryset = Category.objects.filter(user=user)
            
            # If type is already set, filter categories
            if 'type' in self.data:
                transaction_type = self.data.get('type')
                self.fields['category'].queryset = Category.objects.filter(
                    user=user,
                    type=transaction_type
                )
            elif self.instance and self.instance.pk:
                # For update view
                self.fields['category'].queryset = Category.objects.filter(
                    user=user,
                    type=self.instance.type
                )

