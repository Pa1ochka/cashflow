from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Subcategory

class CategoryList(APIView):
    def get(self, request):
        type_id = request.GET.get('type_id')
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')
        return Response({'categories': list(categories)}, status=status.HTTP_200_OK)

class SubcategoryList(APIView):
    def get(self, request):
        category_id = request.GET.get('category_id')
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return Response({'subcategories': list(subcategories)}, status=status.HTTP_200_OK)