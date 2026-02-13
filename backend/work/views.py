
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import viewsets ,decorators,response,status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.



class SkillView(ModelViewSet):
    queryset=Skills.objects.all()
    serializer_class=SkillSerializer
    filter_backends=[filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
        queryset= super().get_queryset()
        query=self.request.query_params.get('q')
        if query:
            queryset=queryset.filter(name__icontains=query)
        
        return queryset[:10]
    
class UserSkillAdd(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=UserSkill.objects.all()
    serializer_class=UserSKillAddSerializer
    
    @decorators.action(detail=False,methods=["get"])    
    def CurrentUserSkills(self,request):
        user=self.request.user
        skills=user.user_skills.all()
        serializer=self.get_serializer(skills,many=True)
        return response.Response(serializer.data)

    
    
    def perform_create(self, serializer):
        
        user = self.request.user
        years_of_experience = self.request.data.get('years_of_experience')
        skill_id = self.request.data.get('skill')
        skill=Skills.objects.get(id=skill_id)
        proficiency = self.request.data.get('proficiency_level')
        proficiency_level = proficiency
        description = self.request.data.get('description')

        serializer.save(
            user=user,
            years_of_experience=years_of_experience,
            skill=skill,
            proficiency_level=proficiency_level,
            description=description
        )
        
    def create(self, request, *args, **kwargs):
        print("Incoming raw data:", request.data)  
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)    
        
    

class WorkOfferViewset(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class=WorkOfferSerializer
    
    def get_queryset(self):
        return WorkOffers.objects.exclude(offered_by=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        offered_by=self.request.user
        description=self.request.data.get('description')
        name=self.request.data.get('name')
        
        serializer.save(
            offered_by=offered_by,
            description=description,
            name=name,  
        )
        
    def create(self, request, *args, **kwargs):
        print("incoming data:",request.data) 
        serializer=self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer) 
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    @decorators.action(detail=False,methods=["get"],permission_classes=[IsAuthenticated])
    def CurrentUserSkillOffers(self,request):
        user=self.request.user
        offers=user.user_offers.all()
        serializer=self.get_serializer(offers,many=True)
        return response.Response(serializer.data)



            
    
        


