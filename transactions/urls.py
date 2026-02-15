from django.urls import path
from . import views

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='edit_transaction'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    path('api/categories/', views.get_categories, name='get_categories'),
]

