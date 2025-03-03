from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import LogInUserSerializer, UserSerializer, RegisterUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken

class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer

class LogInUserView(APIView):
    def post(self, request):
        serializer = LogInUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "user": UserSerializer(user).data,
            }, status=status.HTTP_200_OK)

            response.set_cookie(key="access_token",
                                value=access_token,
                                httponly=True,
                                secure=False,
                                samesite='None')
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=False,
                                samesite='None')
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogOutUserView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"message": "Error invalidating token" + str(e)},
                                status=status.HTTP_401_UNAUTHORIZED)

            response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        else:
            return Response({"message": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"message": "No refresh token provided"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access_token set successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token",
                                value=access_token,
                                httponly=True,
                                secure=False,
                                samesite='None')
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=False,
                                samesite='None')
            
            return response

        except InvalidToken:
            return Response({"message": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
