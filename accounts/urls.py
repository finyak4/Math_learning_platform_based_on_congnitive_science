from django.urls import path, include
from .views import SignUpView, profile_view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
    path('', include('django.contrib.auth.urls')),
]
