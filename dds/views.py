from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

def transaction_list(request):
    transactions = Transaction.objects.all()
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    # Фильтрация
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        try:
            date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%dT%H:%M'))
            transactions = transactions.filter(date__gte=date_from)
        except ValueError:
            pass  # Игнорируем некорректные даты
    if date_to:
        try:
            date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%dT%H:%M'))
            transactions = transactions.filter(date__lte=date_to)
        except ValueError:
            pass  # Игнорируем некорректные даты
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if type_id:
        transactions = transactions.filter(type_id=type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)

    return render(request, 'dds/transaction_list.html', {
        'transactions': transactions,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    })

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'dds/transaction_form.html', {'form': form})

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'dds/transaction_form.html', {'form': form})

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'dds/transaction_list.html', {
        'transactions': Transaction.objects.all(),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

def reference_management(request):
    status_form = StatusForm(prefix='status')
    type_form = TypeForm(prefix='type')
    category_form = CategoryForm(prefix='category')
    subcategory_form = SubcategoryForm(prefix='subcategory')

    if request.method == 'POST':
        if 'status_submit' in request.POST:
            status_form = StatusForm(request.POST, prefix='status')
            if status_form.is_valid():
                status_form.save()
                return redirect('reference_management')
        elif 'type_submit' in request.POST:
            type_form = TypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                return redirect('reference_management')
        elif 'category_submit' in request.POST:
            category_form = CategoryForm(request.POST, prefix='category')
            if category_form.is_valid():
                category_form.save()
                return redirect('reference_management')
        elif 'subcategory_submit' in request.POST:
            subcategory_form = SubcategoryForm(request.POST, prefix='subcategory')
            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('reference_management')

    context = {
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'dds/reference_management.html', context)


def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse({'categories': list(categories)})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})