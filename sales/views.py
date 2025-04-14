from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Sales
from .serializers import SalesSerializer
from .service import create_sales, update_sales, delete_sales, list_sales_by_id
import logging
logger = logging.getLogger(__name__)


class SalesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = create_sales(serializer.validated_data)
        return Response(SalesSerializer(sale).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_object_or_404(Sales, pk=pk)
        serializer = SalesSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = update_sales(instance, serializer.validated_data)
        return Response(SalesSerializer(updated).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Sales, pk=pk)
        delete_sales(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        sale = list_sales_by_id(pk)
        if not sale:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesSerializer(sale)
        return Response(serializer.data)

    # Optional list all sales
    def list(self, request):
        queryset = Sales.objects.all()
        serializer = SalesSerializer(queryset, many=True)
        return Response(serializer.data)