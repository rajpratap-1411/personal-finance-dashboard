from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category

@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """Create default categories when a new user is created"""
    if created:
        # Default income categories
        income_categories = [
            {'name': 'Salary', 'icon': 'briefcase'},
            {'name': 'Freelance', 'icon': 'laptop'},
            {'name': 'Investment', 'icon': 'trending-up'},
            {'name': 'Other Income', 'icon': 'cash'},
        ]

        # Default expense categories
        expense_categories = [
            {'name': 'Food', 'icon': 'restaurant'},
            {'name': 'Transport', 'icon': 'car'},
            {'name': 'Rent', 'icon': 'home'},
            {'name': 'Utilities', 'icon': 'bolt'},
            {'name': 'Shopping', 'icon': 'bag'},
            {'name': 'Entertainment', 'icon': 'film'},
            {'name': 'Healthcare', 'icon': 'heart'},
            {'name': 'Education', 'icon': 'book'},
            {'name': 'Other Expense', 'icon': 'more-horizontal'},
        ]

        for cat_data in income_categories:
            Category.objects.get_or_create(
                user=instance,
                name=cat_data['name'],
                type='income',
                defaults={'icon': cat_data['icon']}
            )

        for cat_data in expense_categories:
            Category.objects.get_or_create(
                user=instance,
                name=cat_data['name'],
                type='expense',
                defaults={'icon': cat_data['icon']}
            )

