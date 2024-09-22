from django.urls import path
from .endpoints import (
    UserRegistrationView, 
    UserLoginView,
    ChatView,
    TokenBalanceView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('tokens/', TokenBalanceView.as_view(), name='token_balance'),
]
