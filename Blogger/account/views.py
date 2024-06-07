from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'data': serializer.errors , 'message' : 'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            
            return Response({'message' : 'Your account is created'},status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({'message' : 'something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data= request.data)
            if not serializer.is_valid():
                return Response({'data': serializer.errors , 'message' : 'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            tokens = serializer.get_tokens_for_user(serializer.data)
            access_token_expired = tokens.get('access_expired', False)
            if access_token_expired:
                # Use refresh token to generate a new access token
                refresh_token = request.COOKIES.get('refresh_token')
                if refresh_token:
                    refresh = RefreshToken(refresh_token)
                    tokens['access'] = str(refresh.access_token)
            
            response = Response({'data':tokens,'message': 'Login successful', 'access_token_expired': access_token_expired})
            ############  front end access####################
            response.set_cookie(key='access_token', value=tokens['access'], httponly=False)
            ############
            response.set_cookie(key='refresh_token', value=tokens['refresh'], httponly=True)
            return response
            
        except Exception as e:
            print(e)
            return Response({'data': {},'message' : 'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({'message': 'Missing refresh token'}, status=400)

            # Blacklist the provided refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logged out successfully'}, status=200)

        except Exception as e:
            print(e)  
            return Response({'message': 'An error occurred during logout'}, status=500)
