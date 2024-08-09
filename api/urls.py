from django.urls import path
from api.views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
    path('search/', BookSearchAPIView.as_view(), name='book_search'),
    path('recommendations/submit/', SubmitRecommendationAPIView.as_view(), name='submit_recommendation'),
    path('recommendations/', ListRecommendationsAPIView.as_view(), name='list_recommendations'),
]