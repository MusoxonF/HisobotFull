from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
    TokenBlacklistView, TokenRefreshSlidingView,
    TokenObtainSlidingView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify_View'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist_View'),
    path('refresh_sliding/', TokenRefreshSlidingView.as_view(), name='token_refresh_sliding_View'),
    path('obtain_sliding/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding_View'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/<int:id>/', SignUpDetail.as_view(), name='signup_detail'),
    path('xodim/', XodimView.as_view(), name='xodim'),
    path('xodim/<int:id>/', XodimDetail.as_view(), name='xodim_detail'),
    path('change/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
]