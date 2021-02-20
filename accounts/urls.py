from django.urls import path
from .views import login_view, logout_view, register_view, user_update_view, user_delete_view, contact_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('update/', user_update_view, name='update'),
    path('delete/', user_delete_view, name='delete'),
    path('contact/', contact_view, name='contact'),
]
