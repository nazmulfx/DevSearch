
from django.db.models import Q
from . models import Profile, Skill

def SearchProfiles(request):
    search_query = ''                                   # Default Search filter is ''= empty (we will search developer name)
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')  # checked is there any search
    print(search_query)
    
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(       # distinct() used for, eliminate duplicates rows from the query result.
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)                             # query child objects profile>skill, query does the profile have search sills
    )                                                   # filtering data by name (in model, name=developer name), icontains means case sensitivity
    return profiles, search_query