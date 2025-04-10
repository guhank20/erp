from django.urls import path

from .views import create_role, list_role, update_role, delete_role, user_register, user_login, logout, update_user_by_id, user_list

urlpatterns = [
    path('roles/create/', create_role, name='create-role'),
    path('roles/lists/', list_role, name='list-role'),
    path('roles/update/<int:id>/', update_role, name='update-role'),
    path('roles/delete/<int:id>/', delete_role, name='delete-role'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('user/update/<int:user_id>/', update_user_by_id, name='update_user_by_id'),
    path('user/list/', user_list, name='user-list')

]
