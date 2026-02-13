from django.urls import path

from . import views
from .api import views as api_views
from .api.routers import router


app_name = 'users'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),

    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-complete/', name='password_reset_complete'),

    path('users-cart/', views.UsersCartView.as_view(), name='users_cart'),


    path('api/registration/', api_views.UserRegistrationAPIView.as_view(), name='registration'),
    path('api/token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]


urlpatterns += router.urls