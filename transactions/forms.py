from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'description', 'date']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_type',
                'onchange': 'updateCategories()'
            }),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Enter amount'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description'
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

