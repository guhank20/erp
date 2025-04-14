from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Purchase
from .serializers import PurchaseSerializer
from .service import create_purchase, update_purchase, delete_purchase, list_purchase_by_id
import logging
logger = logging.getLogger(__name__)


class PurchaseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = create_purchase(serializer.validated_data)
        return Response(PurchaseSerializer(sale).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_object_or_404(Purchase, pk=pk)
        serializer = PurchaseSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = update_purchase(instance, serializer.validated_data)
        return Response(PurchaseSerializer(updated).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Purchase, pk=pk)
        delete_purchase(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        sale = list_purchase_by_id(pk)
        if not sale:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseSerializer(sale)
        return Response(serializer.data)

    # Optional list all Purchase
    def list(self, request):
        queryset = Purchase.objects.all()
        serializer = PurchaseSerializer(queryset, many=True)
        return Response(serializer.data)