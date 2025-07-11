from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')