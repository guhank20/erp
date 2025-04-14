from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import WarehouseSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from . import service
from rest_framework.decorators import api_view

from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from inventory.models import Inventory
from inventory.serializers import InventorySerializer
from inventory.service import create_inventory, update_inventory, delete_inventory, transaction_items
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class WarehouseListCreateView(APIView):
    def get(self, request):
        warehouse = service.get_all_warehouses()
        serializer = WarehouseSerializer(warehouse, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            warehouse = service.create_warehouse(serializer.validated_data)
            return Response(WarehouseSerializer(warehouse).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventory.objects.filter(active=True)

    def perform_create(self, serializer):
        try:
            validated_data = serializer.validated_data
            instance = create_inventory(validated_data)
            serializer.instance = instance
        except ValidationError as e:
            raise DRFValidationError(e)

    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            validated_data = serializer.validated_data
            updated = update_inventory(instance, validated_data)
           
            serializer.instance = updated
        except ValidationError as e:
            raise DRFValidationError(e)

    def perform_destroy(self, instance):
        delete_inventory(instance)

@api_view(['GET'])
def transaction_item_list_view(request):
    data = transaction_items(request)
    #data = {"message": "Hello, World!"}
    return Response(data)
