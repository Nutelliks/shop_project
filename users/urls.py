from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='change_password'),

    path('users-cart/', views.UsersCartView.as_view(), name='users_cart'),
]
