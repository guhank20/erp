from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializers, UserSerializer, UserListSerializer
from django.db import IntegrityError, transaction
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def create_role(request):
    serializer = RoleSerializers(data=request.data)

    if serializer.is_valid():
        role_name = serializer.validated_data.get("name")

        # Manually check for existing role before saving
        if Role.objects.filter(name=role_name).exists():
            return Response({"error": "Role with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():  # Ensures ID is not incremented on failure
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_role(request):
    roles = Role.objects.all().order_by('id')
    serializer = RoleSerializers(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_role(request, id):
    data = request.data

    # Check if role exists
    if not Role.objects.filter(id=id).exists():
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
    
    name = request.data.get('name')
    description = request.data.get('description')

    # Prepare the update dictionary
    update_data = {}
    if name:
        update_data['name'] = name
    if description:
        update_data['description'] = description

    if not update_data:  # If both name & description are missing, return an error
        return Response({"error": "At least one field (name or description) is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            updated_count = Role.objects.filter(id=id).update(**update_data)  # Direct DB update

            if updated_count == 0:
                return Response({"error": "No fields updated"}, status=status.HTTP_400_BAD_REQUEST)

            updated_role = Role.objects.get(id=id)  # Fetch updated role
            serializer = RoleSerializers(updated_role)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except IntegrityError:
        return Response({"error": "Role with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_role(request, id):
    if not Role.objects.filter(id=id).exists():
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        with transaction.atomic():  # Ensures data integrity
            role = Role.objects.get(id=id)
            role.delete()
            return Response({"message": "Role deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
def user_register(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    role_id = request.data.get('role_id')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not phone_number or not password or not role_id or not first_name or not last_name:
        return Response({"error": "Phone number, password, role, first name and last name are required."}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(phone_number=phone_number).exists():
        return Response({"error": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
    user = CustomUser.objects.create_user(phone_number=phone_number, password=password, role_id=role_id,first_name=first_name,last_name=last_name)

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "User registered successfully",
        "token": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def user_login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    user = authenticate(phone_number=phone_number, password=password)
    if user is None:
        return Response({"error": "Invalid phone number or password."}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "token": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)
        
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the token
        
        return Response({"message": "Successfully logged out"}, status=200)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_by_id(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    first_name = data.get("first_name", user.first_name)
    last_name = data.get("last_name", user.last_name)
    role_id = data.get("role_id", user.role_id)  # Optional role update
    password = data.get("password", None)  # Check if password update is requested
    phone_number = data.get("phone_number", user.phone_number)

    try:
        
        user.first_name = first_name
        user.last_name = last_name
        user.role_id = role_id
        user.phone_number = phone_number

        if password:
            user.set_password(password)  # Hash the new password before saving

        user.save()

        serializer = UserSerializer(user)  # Serialize updated user
        return Response(serializer.data, status=status.HTTP_200_OK)
    except IntegrityError as e:
        return Response({"error": "Update failed due to a database error.", 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = CustomUser.objects.all()

    serializer = UserListSerializer(users, many= True)
    return Response(serializer.data, status=status.HTTP_200_OK)

