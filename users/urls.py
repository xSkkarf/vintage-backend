from django.urls import path
from users.views import UserInfoView, RegisterUserView, LogInUserView, LogOutUserView, CookieTokenRefreshView

urlpatterns = [
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('login/', LogInUserView.as_view(), name='user-login'),
    path('logout/', LogOutUserView.as_view(), name='user-logout'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token-refresh'),
]