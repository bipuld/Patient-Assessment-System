from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import signup, LoginApiView, GetUserProfile, LogoutApiView

urlpatterns = [
    # User Authentication APIs
    path('api/signup/', signup, name='signup'),  # User signup endpoint
    path('api/login/', LoginApiView.as_view(), name='login'),  # User login endpoint
    path('api/get-profile/', GetUserProfile.as_view(), name='get_profile'),  # Get user profile endpoint
    path('api/logout/', LogoutApiView.as_view(), name='logout'),  # User logout endpoint

    # JWT Token APIs
    path('api/login-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
    path('api/login-token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Token verify endpoint
]
