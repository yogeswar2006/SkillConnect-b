from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes , api_view
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
from .serializers import QueryUsersSerializer
from rest_framework.response import Response
from .models import FriendRequest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from django.db import models
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def QueryUsers(request,query=None):
    current_user = request.user
    
    
    users =CustomUser.objects.filter(username__icontains=query).exclude(id=current_user.id).order_by('-created_at') 
    serializer = QueryUsersSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendFriendRequest(request):
     receiver_id = request.data.get('receiver_id')
     
     if receiver_id==request.user.id:
         return Response({'error':'cannot send to yourself'},status=400)
     
     receiver = CustomUser.objects.get(id=receiver_id)
     friend_request , created = FriendRequest.objects.get_or_create(
         sender=request.user,
         receiver=receiver,
         defaults={"status":"pending"}
     )
     
     if not created:
         if friend_request.status=="pending":
             return Response({'message':'friend request already sent'},status=200)
         if friend_request.status=="accepted":
             return Response({'message':'You are already frineds '},status=400)
         if friend_request.status=="declined":
            friend_request.status="pending"
            friend_request.save()
            
     profile_image=None            
     if request.user.profile_img:
         profile_image=request.user.profile_img.url
         
         
     
            
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
            f"user_{receiver.id}",
            {
                "type": "friend_request",
                "id": friend_request.id,
                "sender_id": request.user.id,
                "sender_username": request.user.username,
                'sender_profile_image':profile_image
            }
        )
            
     
     return Response({'message':'Friend request sent'})            
 
 

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AcceptFriendRequest(request):
    request_id = request.data.get("request_id")

    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status="pending"
    )

    
    friend_request.status = "accepted"
    friend_request.save()

    
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{friend_request.sender.id}",
        {
            "type": "friend_request_accepted",
            "by_user_id": request.user.id,
            "by_username": request.user.username,
        }
    )

    return Response({"message": "Friend request accepted"})



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def DeclineFriendRequest(request):
    request_id = request.data.get("request_id")

    if not request_id:
        return Response({"error": "request_id required"}, status=400)

    fr = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status="pending",
    )

    #  update status
    fr.status = "declined"
    fr.save()

    # #  notify sender
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f"user_{sender_id}",
    #     {
    #         "type": "friend_request_declined",
    #         "by_user_id": request.user.id,
    #         "by_username": request.user.username,
    #     }
    # )

    return Response({"message": "Friend request declined"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchPendingRequests(request):
    current_user = request.user
    
    requests = FriendRequest.objects.filter(
        receiver = current_user,
        status = 'pending'
        
    ).select_related('sender')
    
    data = [ {
              "id": fr.id, 
            "sender_id":fr.sender.id,
            "sender_username":fr.sender.username,
            "sender_profile_image":(
                fr.sender.profile_img.url if fr.sender.profile_img else None
            )
            
        }  for fr in requests]
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FriendsList(request):
    current_user = request.user
    friends_requests = FriendRequest.objects.filter(
        status="accepted"
    ).filter(
        models.Q(sender=current_user) | models.Q(receiver=current_user)
    ).select_related('sender','receiver')
    
    friends = []

    for fr in friends_requests:
        friend = fr.receiver if fr.sender == current_user else fr.sender

        friends.append({
            "id": friend.id,
            "username": friend.username,
            "profile_image": (
                friend.profile_img.url if friend.profile_img else None
            ),
        })
    
    return Response(friends)    