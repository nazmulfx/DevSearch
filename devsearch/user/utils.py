
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Profile, Skill


def paginateProfiles(request, profiles, objectPerPage):
    
    page = request.GET.get('page')                      # getting data from user like ?page=1
    #objectPerPage = 3
    paginator = Paginator(profiles, objectPerPage)
    
    try:                                                # if everything is good like url/?page=2
        profiles = paginator.page(page)                 
    except PageNotAnInteger:                            # if page number not given like url/
        page = 3
        profiles = paginator.page(page)
    except EmptyPage:                                   # if user accidently goes wrong page number like url/?page=100000
        page = paginator.num_pages
        profiles = paginator.page(page)
        
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
        
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, profiles


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