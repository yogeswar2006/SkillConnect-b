from django.contrib import admin

# Register your models here.

from . models import UserSkill,WorkMatches,WorkOffers,WorkRequests,Skills

admin.site.register(UserSkill)
admin.site.register(WorkMatches)
admin.site.register(WorkOffers)
admin.site.register(WorkRequests)
admin.site.register(Skills)
