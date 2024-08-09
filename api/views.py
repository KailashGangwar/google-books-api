from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import *
from django.contrib.auth import authenticate
from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.signing import Signer, BadSignature
from django.http import HttpResponseForbidden
from .permissions import IsOpsUser, IsClientUser
from rest_framework import generics
from .models import BookRecommendation
from .serializers import BookRecommendationSerializer
from .utils import fetch_book_data
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  
class BookSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        api_key = 'your_google_books_api_key' 
        if query:
            data = fetch_book_data(query, api_key)
            if data:
                return Response(data)
            return Response({'error': 'Failed to fetch data from Google Books'}, status=500)
        return Response({'error': 'No query provided'}, status=400)


class SubmitRecommendationAPIView(generics.CreateAPIView):
    queryset = BookRecommendation.objects.all()
    serializer_class = BookRecommendationSerializer

class ListRecommendationsAPIView(generics.ListAPIView):
    queryset = BookRecommendation.objects.all()
    serializer_class = BookRecommendationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get('genre')
        rating = self.request.query_params.get('rating')
        if genre:
            queryset = queryset.filter(genre=genre)
        if rating:
            queryset = queryset.filter(rating__gte=rating)
        return queryset.order_by('-created_at')

