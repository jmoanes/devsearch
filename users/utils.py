from .models import Profile, Skill
from django.db.models import Q



def searchProfile(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query) # Search Skill

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)|
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        ) 

    return profiles, search_query