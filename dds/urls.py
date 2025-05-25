from django.urls import path
from . import views
from .api import CategoryList, SubcategoryList

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    path('references/', views.reference_management, name='reference_management'),
    path('status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:pk>/', views.status_delete, name='status_delete'),
    path('type/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('type/delete/<int:pk>/', views.type_delete, name='type_delete'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/categories/', CategoryList.as_view(), name='api_categories'),
    path('api/subcategories/', SubcategoryList.as_view(), name='api_subcategories'),
]