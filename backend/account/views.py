from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view , permission_classes
from django.contrib.auth import logout
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

# Create your views here.


class Userview(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer
    
class CookieTokenObtainView(TokenObtainPairView):
    def post(self,request,*args, **kwargs):
        response = super().post(request,*args,**kwargs)
        
        if response.status_code == 200:
                refresh = response.data['refresh']
                access = response.data['access']
                
                response.set_cookie(
                    key='refresh_token',
                    value=refresh,
                    httponly=True,
                    secure=settings.AUTH_COOKIE_SECURE,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                    path='/'
                )
                
                response.set_cookie(
                    key='access_token',
                    value=access,
                    httponly=True,
                    secure=settings.AUTH_COOKIE_SECURE,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                    path='/'
                )
                
                del response.data['refresh']
               
        return response                

class CookieTokenRefreshView(TokenRefreshView):
    def post(self,request,*args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail":"No refresh token cookie"},status=status.HTTP_401_UNAUTHORIZED)
        request.data['refresh']=refresh_token
    
        try:
            response = super().post(request,*args,**kwargs)
            
            
        except(InvalidToken, TokenError):
            return Response({"datail":"invalid refresh token or token error"},
                            status=status.HTTP_401_UNAUTHORIZED)
            
        
        access = response.data.get('access')
        
        response.set_cookie(
            key='access_token',
            value =access,
            httponly=True,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            secure=settings.AUTH_COOKIE_SECURE,
            path='/'
        )
        
        
        response.data = {'detail':'Token refreshed','success':True
                        }
        
        return response

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response(
            {"detail": "Successfully logged out", "success": True},
            status=status.HTTP_200_OK,
        )

        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")

        return response



@method_decorator(csrf_exempt, name="dispatch")
class CurrentUserView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        
        profile_img = ((request.user.profile_img)
                        if request.user.profile_img
                        else None
        )

        response =Response(
            {'id':request.user.id,
             'username':request.user.username,
             'email':request.user.email,
             'bio':request.user.bio,
             'first_name':request.user.first_name,
             'last_name':request.user.last_name,
             'profile_img':profile_img
             }
            
        )
        
        return response
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateProfile(request):
    user = request.user
    
    user.username = request.data.get('username',user.username)
    user.email = request.data.get('email',user.email)
    user.first_name = request.data.get('first_name',user.first_name)
    user.last_name = request.data.get('last_name',user.last_name)
    user.bio = request.data.get('bio',user.bio)   
    
    user.save()
    
    profile_img = ((request.user.profile_img)
                        if request.user.profile_img
                        else None
        )

    response =Response(
            {'id':request.user.id,
             'username':request.user.username,
             'email':request.user.email,
             'bio':request.user.bio,
             'first_name':request.user.first_name,
             'last_name':request.user.last_name,
             'profile_img':profile_img
             }
            
        )
        
    return response