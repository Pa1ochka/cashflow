from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from django.contrib import messages

# Отображение списка транзакций с фильтрацией
def transaction_list(request):
    transactions = Transaction.objects.all()
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    # Фильтрация по параметрам GET
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
            messages.error(request, "Некорректный формат даты (от).")
    if date_to:
        try:
            date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%dT%H:%M'))
            transactions = transactions.filter(date__lte=date_to)
        except ValueError:
            messages.error(request, "Некорректный формат даты (до).")
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

# Создание новой транзакции
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Транзакция успешно создана.")
            return redirect('transaction_list')
        else:
            messages.error(request, "Ошибка при создании транзакции. Проверьте введённые данные.")
    else:
        form = TransactionForm()
    return render(request, 'dds/transaction_form.html', {'form': form})

# Редактирование существующей транзакции
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Транзакция успешно обновлена.")
            return redirect('transaction_list')
        else:
            messages.error(request, "Ошибка при редактировании транзакции. Проверьте введённые данные.")
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'dds/transaction_form.html', {'form': form})

# Удаление транзакции
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Транзакция успешно удалена.")
        return redirect('transaction_list')
    return render(request, 'dds/transaction_list.html', {
        'transactions': Transaction.objects.all(),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

# Управление справочниками
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
                messages.success(request, "Статус успешно добавлен.")
                return redirect('reference_management')
            else:
                messages.error(request, "Ошибка при добавлении статуса. Проверьте данные.")
        elif 'type_submit' in request.POST:
            type_form = TypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                messages.success(request, "Тип успешно добавлен.")
                return redirect('reference_management')
            else:
                messages.error(request, "Ошибка при добавлении типа. Проверьте данные.")
        elif 'category_submit' in request.POST:
            category_form = CategoryForm(request.POST, prefix='category')
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Категория успешно добавлена.")
                return redirect('reference_management')
            else:
                messages.error(request, "Ошибка при добавлении категории. Проверьте данные.")
        elif 'subcategory_submit' in request.POST:
            subcategory_form = SubcategoryForm(request.POST, prefix='subcategory')
            if subcategory_form.is_valid():
                subcategory_form.save()
                messages.success(request, "Подкатегория успешно добавлена.")
                return redirect('reference_management')
            else:
                messages.error(request, "Ошибка при добавлении подкатегории. Проверьте данные.")

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

# Редактирование статуса
def status_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно обновлён.")
            return redirect('reference_management')
        else:
            messages.error(request, "Ошибка при редактировании статуса. Проверьте данные.")
    else:
        form = StatusForm(instance=status)
    return render(request, 'dds/reference_form.html', {'form': form, 'title': 'Редактировать статус'})

# Удаление статуса
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        try:
            status.delete()
            messages.success(request, "Статус успешно удалён.")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении статуса: {str(e)}")
        return redirect('reference_management')
    return render(request, 'dds/reference_management.html', {
        'status_form': StatusForm(prefix='status'),
        'type_form': TypeForm(prefix='type'),
        'category_form': CategoryForm(prefix='category'),
        'subcategory_form': SubcategoryForm(prefix='subcategory'),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

# Редактирование типа
def type_edit(request, pk):
    type_obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Тип успешно обновлён.")
            return redirect('reference_management')
        else:
            messages.error(request, "Ошибка при редактировании типа. Проверьте данные.")
    else:
        form = TypeForm(instance=type_obj)
    return render(request, 'dds/reference_form.html', {'form': form, 'title': 'Редактировать тип'})

# Удаление типа
def type_delete(request, pk):
    type_obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        try:
            type_obj.delete()
            messages.success(request, "Тип успешно удалён.")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении типа: {str(e)}")
        return redirect('reference_management')
    return render(request, 'dds/reference_management.html', {
        'status_form': StatusForm(prefix='status'),
        'type_form': TypeForm(prefix='type'),
        'category_form': CategoryForm(prefix='category'),
        'subcategory_form': SubcategoryForm(prefix='subcategory'),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

# Редактирование категории
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория успешно обновлена.")
            return redirect('reference_management')
        else:
            messages.error(request, "Ошибка при редактировании категории. Проверьте данные.")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dds/reference_form.html', {'form': form, 'title': 'Редактировать категорию'})

# Удаление категории
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, "Категория успешно удалена.")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении категории: {str(e)}")
        return redirect('reference_management')
    return render(request, 'dds/reference_management.html', {
        'status_form': StatusForm(prefix='status'),
        'type_form': TypeForm(prefix='type'),
        'category_form': CategoryForm(prefix='category'),
        'subcategory_form': SubcategoryForm(prefix='subcategory'),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

# Редактирование подкатегории
def subcategory_edit(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, "Подкатегория успешно обновлена.")
            return redirect('reference_management')
        else:
            messages.error(request, "Ошибка при редактировании подкатегории. Проверьте данные.")
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'dds/reference_form.html', {'form': form, 'title': 'Редактировать подкатегорию'})

# Удаление подкатегории
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        try:
            subcategory.delete()
            messages.success(request, "Подкатегория успешно удалена.")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении подкатегории: {str(e)}")
        return redirect('reference_management')
    return render(request, 'dds/reference_management.html', {
        'status_form': StatusForm(prefix='status'),
        'type_form': TypeForm(prefix='type'),
        'category_form': CategoryForm(prefix='category'),
        'subcategory_form': SubcategoryForm(prefix='subcategory'),
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

# API для получения категорий по типу
def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse({'categories': list(categories)})

# API для получения подкатегорий по категории
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})