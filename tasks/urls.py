from django.urls import path
from .views import task_list, create_task, update_task, delete_task, register, user_login, user_logout

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('update/<int:task_id>/', update_task, name='update_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
