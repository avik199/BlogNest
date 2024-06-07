from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import status

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if access token has expired
        if 'token_not_valid' in response.data:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                try:
                    # Use refresh token to generate a new access token
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)
                    response.data['access'] = new_access_token
                    # Set the new access token in cookies
                    response.set_cookie(key='access_token', value=new_access_token, httponly=True)
                except Exception as e:
                    # Handle token refresh failure
                    print("Error refreshing access token:", e)
                    return JsonResponse({'message': 'Token refresh failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return response
