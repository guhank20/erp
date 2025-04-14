from rest_framework import serializers
from inventory.serializers import TransactionItemSerializer
from .models import Purchase
from users.models import CustomUser
from users.serializers import UserListSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True, source='get_items', read_only=True)  # For reading
    item_inputs = TransactionItemSerializer(many=True, write_only=True)  
    # user_id = serializers.PrimaryKeyRelatedField(
    #     queryset=CustomUser.objects.all(),
    #     source='user'
    # )
    # user = UserListSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'supplier_name', 'status', 'purchase_date', 'items','item_inputs']
