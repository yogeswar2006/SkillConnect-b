from django.urls import path,include
from .views import QueryUsers,SendFriendRequest,AcceptFriendRequest,DeclineFriendRequest
from .views import FetchPendingRequests,FriendsList

urlpatterns =[
    path("decline/friendrequest/", DeclineFriendRequest,name='declinedrequest'),
      path('fetch/pending/',FetchPendingRequests,name='pendingrequests'),
    path('search/<str:query>/',QueryUsers,name='queryUsers'),
    path('send/friendrequest/',SendFriendRequest,name='friendrequest'),
    path('accept/friendrequest/',AcceptFriendRequest,name='acceptedrequest'),
     path('fetch/friends/',FriendsList,name='friends')
   
]