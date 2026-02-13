from django.urls import path , re_path,include
from rest_framework.routers import DefaultRouter
from .views import SkillView,UserSkillAdd,WorkOfferViewset

router=DefaultRouter()

router.register(f'skills',SkillView,basename='skills')
router.register(f'addSkill',UserSkillAdd,basename='add_skill')
router.register(f'workOffer',WorkOfferViewset,basename='WorkOffer')




urlpatterns=[
    path('all/',include(router.urls))
    
]