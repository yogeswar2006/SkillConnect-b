from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Userview,CookieTokenObtainView,CookieTokenRefreshView,LogoutView,CurrentUserView
from .views import UpdateProfile
router = DefaultRouter()

router.register(r'register',Userview,basename="register")


urlpatterns =[
    path('user/',include(router.urls)),
    path("token/", CookieTokenObtainView.as_view(), name="token"),
    path('token/refresh/',CookieTokenRefreshView.as_view(),name = "token_refresh"),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('auth/me/',CurrentUserView.as_view(),name = 'currentuser'),
    path('update/profile/',UpdateProfile,name='profileUpdate')
]