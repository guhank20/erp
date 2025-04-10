from rest_framework import serializers

from inventory.models import Warehouse, Inventory, TransactionItem


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'uuid', 'name', 'location','capacity']

class InventorySerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset = Warehouse.objects.all(), source='warehouse'
    )
    class Meta:
        model = Inventory
        fields = ['id', 'uuid','product_name', 'quantity','category', 'warehouse', 'warehouse_id', 'price','available_qty','threshold','active']

class MinimalInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'uuid', 'product_name']

class TransactionItemSerializer(serializers.ModelSerializer):
    product = MinimalInventorySerializer(read_only=True)
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = TransactionItem
        fields = ['id', 'product', 'quantity', 'per_price', 'price', 'content_type']

    def get_content_type(self, obj):
        return obj.content_type.model
        