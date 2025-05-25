from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Status, Type, Category, Subcategory, Transaction
from .forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from datetime import datetime
import json


class ModelTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Бизнес")
        self.type = Type.objects.create(name="Списание")
        self.category = Category.objects.create(name="Инфраструктура", type=self.type)
        self.subcategory = Subcategory.objects.create(name="VPS", category=self.category)

    def test_status_str(self):
        self.assertEqual(str(self.status), "Бизнес")

    def test_type_str(self):
        self.assertEqual(str(self.type), "Списание")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Инфраструктура")

    def test_subcategory_str(self):
        self.assertEqual(str(self.subcategory), "VPS")

    def test_transaction_str(self):
        transaction = Transaction.objects.create(
            date=timezone.make_aware(datetime(2025, 5, 24, 14, 30)),
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=5000.00,
            comment="Оплата сервера"
        )
        expected_str = f"2025-05-24 14:30 - 5000.00 (Списание)"
        self.assertEqual(str(transaction), expected_str)



    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            date=timezone.make_aware(datetime(2025, 5, 24, 14, 30)),
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=5000.00,
            comment="Оплата сервера"
        )
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(transaction.amount, 5000.00)

class FormTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Бизнес")
        self.type = Type.objects.create(name="Списание")
        self.category = Category.objects.create(name="Инфраструктура", type=self.type)
        self.subcategory = Subcategory.objects.create(name="VPS", category=self.category)

    def test_transaction_form_valid(self):
        form_data = {
            'date': '2025-05-24T14:30',
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '5000.00',
            'comment': 'Оплата сервера'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transaction_form_invalid(self):
        form_data = {
            'date': '2025-05-24T14:30',
            'status': self.status.id,
            'type': self.type.id,
            'category': '',  # Пустая категория
            'subcategory': self.subcategory.id,
            'amount': '5000.00',
            'comment': 'Оплата сервера'
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_transaction_form_aware_date(self):
        form_data = {
            'date': timezone.make_aware(datetime(2025, 5, 24, 14, 30)).strftime('%Y-%m-%dT%H:%M'),
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '5000.00',
            'comment': 'Оплата сервера'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['date'].tzinfo is not None)

    def test_transaction_form_invalid_date(self):
        form_data = {
            'date': 'invalid-date',
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '5000.00',
            'comment': 'Оплата сервера'
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_status_form_valid(self):
        form_data = {'name': 'Личное'}
        form = StatusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_type_form_valid(self):
        form_data = {'name': 'Пополнение'}
        form = TypeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_valid(self):
        form_data = {'name': 'Маркетинг', 'type': self.type.id}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subcategory_form_valid(self):
        form_data = {'name': 'Proxy', 'category': self.category.id}
        form = SubcategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.status = Status.objects.create(name="Бизнес")
        self.type = Type.objects.create(name="Списание")
        self.category = Category.objects.create(name="Инфраструктура", type=self.type)
        self.subcategory = Subcategory.objects.create(name="VPS", category=self.category)
        self.transaction = Transaction.objects.create(
            date=timezone.make_aware(datetime(2025, 5, 24, 14, 30)),
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=5000.00,
            comment="Оплата сервера"
        )

    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/transaction_list.html')
        self.assertContains(response, "Оплата сервера")
        self.assertContains(response, "5000,00")  # Учитываем русскую локализацию

    def test_transaction_list_filter(self):
        response = self.client.get(reverse('transaction_list'), {
            'date_from': timezone.make_aware(datetime(2025, 5, 24, 14, 0)).strftime('%Y-%m-%dT%H:%M'),
            'date_to': timezone.make_aware(datetime(2025, 5, 24, 15, 0)).strftime('%Y-%m-%dT%H:%M'),
            'status': self.status.id,
            'type': self.type.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Оплата сервера")
        self.assertNotContains(response, "Транзакции не найдены")

    def test_transaction_list_filter_category(self):
        response = self.client.get(reverse('transaction_list'), {
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Инфраструктура")
        self.assertNotContains(response, "Транзакции не найдены")

    def test_transaction_list_filter_subcategory(self):
        response = self.client.get(reverse('transaction_list'), {
            'subcategory': self.subcategory.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VPS")
        self.assertNotContains(response, "Транзакции не найдены")

    def test_transaction_list_filter_invalid_date(self):
        response = self.client.get(reverse('transaction_list'), {
            'date_from': 'invalid-date',
            'date_to': timezone.make_aware(datetime(2025, 5, 24, 15, 0)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Оплата сервера")  # Фильтр игнорирует некорректную дату

    def test_transaction_create_view_get(self):
        response = self.client.get(reverse('transaction_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/transaction_form.html')

    def test_transaction_create_view_post(self):
        form_data = {
            'date': timezone.make_aware(datetime(2025, 5, 24, 15, 0)).strftime('%Y-%m-%dT%H:%M'),
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '6000.00',
            'comment': 'Оплата VPS'
        }
        response = self.client.post(reverse('transaction_create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to transaction_list
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertTrue(Transaction.objects.filter(comment="Оплата VPS").exists())

    def test_transaction_create_view_post_invalid(self):
        form_data = {
            'date': 'invalid-date',
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '6000.00',
            'comment': 'Оплата VPS'
        }
        response = self.client.post(reverse('transaction_create'), form_data)
        self.assertEqual(response.status_code, 200)  # Остаётся на форме
        self.assertEqual(Transaction.objects.count(), 1)  # Транзакция не создана

    def test_transaction_edit_view_get(self):
        response = self.client.get(reverse('transaction_edit', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/transaction_form.html')

    def test_transaction_edit_view_post(self):
        form_data = {
            'date': timezone.make_aware(datetime(2025, 5, 24, 15, 30)).strftime('%Y-%m-%dT%H:%M'),
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '7000.00',
            'comment': 'Обновлённая оплата'
        }
        response = self.client.post(reverse('transaction_edit', args=[self.transaction.id]), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to transaction_list
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 7000.00)
        self.assertEqual(self.transaction.comment, "Обновлённая оплата")

    def test_transaction_edit_view_post_invalid(self):
        form_data = {
            'date': 'invalid-date',
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '7000.00',
            'comment': 'Обновлённая оплата'
        }
        response = self.client.post(reverse('transaction_edit', args=[self.transaction.id]), form_data)
        self.assertEqual(response.status_code, 200)  # Остаётся на форме
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 5000.00)  # Сумма не изменилась

    def test_transaction_delete_view(self):
        response = self.client.post(reverse('transaction_delete', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to transaction_list
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_delete_view_get(self):
        response = self.client.get(reverse('transaction_delete', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/transaction_list.html')

    def test_reference_management_view_get(self):
        response = self.client.get(reverse('reference_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dds/reference_management.html')

    def test_reference_management_view_post_status(self):
        form_data = {'status-name': 'Личное', 'status_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to reference_management
        self.assertTrue(Status.objects.filter(name="Личное").exists())

    def test_reference_management_view_post_type(self):
        form_data = {'type-name': 'Пополнение', 'type_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to reference_management
        self.assertTrue(Type.objects.filter(name="Пополнение").exists())

    def test_reference_management_view_post_category(self):
        form_data = {'category-name': 'Маркетинг', 'category-type': self.type.id, 'category_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to reference_management
        self.assertTrue(Category.objects.filter(name="Маркетинг").exists())

    def test_reference_management_view_post_subcategory(self):
        form_data = {'subcategory-name': 'Proxy', 'subcategory-category': self.category.id, 'subcategory_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to reference_management
        self.assertTrue(Subcategory.objects.filter(name="Proxy").exists())

    def test_reference_management_view_post_status_invalid(self):
        form_data = {'status-name': '', 'status_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 200)  # Остаётся на той же странице
        self.assertContains(response, "Обязательное поле")  # Проверка ошибки формы

    def test_reference_management_view_post_type_invalid(self):
        form_data = {'type-name': '', 'type_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Обязательное поле")

    def test_reference_management_view_post_category_invalid(self):
        form_data = {'category-name': '', 'category-type': '', 'category_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Обязательное поле")

    def test_reference_management_view_post_subcategory_invalid(self):
        form_data = {'subcategory-name': '', 'subcategory-category': '', 'subcategory_submit': '1'}
        response = self.client.post(reverse('reference_management'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Обязательное поле")

    def test_get_categories_view(self):
        response = self.client.get(reverse('get_categories'), {'type_id': self.type.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['categories']), 1)
        self.assertEqual(data['categories'][0]['name'], "Инфраструктура")

    def test_get_categories_view_invalid_type(self):
        response = self.client.get(reverse('get_categories'), {'type_id': 999})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['categories']), 0)

    def test_get_subcategories_view(self):
        response = self.client.get(reverse('get_subcategories'), {'category_id': self.category.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['subcategories']), 1)
        self.assertEqual(data['subcategories'][0]['name'], "VPS")

    def test_get_subcategories_view_invalid_category(self):
        response = self.client.get(reverse('get_subcategories'), {'category_id': 999})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['subcategories']), 0)