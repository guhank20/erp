from rest_framework import serializers
from .models import Role
from .models import CustomUser, Role

class RoleSerializers(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, 
        required=True, 
        allow_blank=False, 
        error_messages={"blank": "Role name cannot be empty.", "required": "Role name is required."}
    )
    description = serializers.CharField(
        required=True,
        error_messages={"required": "Description name is required."}
    )
    class Meta:
        model = Role
        fields = ['id', 'uuid', 'name', 'description']

    def create(self, validated_data):
        """Explicitly define how a Role is created."""
        return Role.objects.create(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'role_id']  # Add necessary fields
        #extra_kwargs = {'phone_number': {'read_only': True}}  # Prevent phone number updates if needed

    def update(self, instance, validated_data):
        """ Update only fields present in the request """
        for key, value in validated_data.items():
            setattr(instance, key, value)  # Dynamically set only provided fields

        instance.save()
        return instance

class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','uuid','first_name', 'last_name', 'phone_number', 'role_id','role_name']  # Add necessary fields
    def get_role_name(self, obj):
        """ Fetch role name from Role model based on role_id """
        role = Role.objects.filter(id=obj.role_id).first()  # Get role instance
        return role.name if role else None


