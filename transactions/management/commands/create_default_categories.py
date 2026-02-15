from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transactions.models import Category

class Command(BaseCommand):
    help = 'Create default categories for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create categories for')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

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

        created_count = 0
        for cat_data in income_categories:
            category, created = Category.objects.get_or_create(
                user=user,
                name=cat_data['name'],
                type='income',
                defaults={'icon': cat_data['icon']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created income category: {cat_data["name"]}'))

        for cat_data in expense_categories:
            category, created = Category.objects.get_or_create(
                user=user,
                name=cat_data['name'],
                type='expense',
                defaults={'icon': cat_data['icon']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created expense category: {cat_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal categories created: {created_count}'))

