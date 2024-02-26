
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Project, Tag


def paginateProjects(request, projects, objectPerPage):

    #### Paginator Setup in My Way ####
    page = request.GET.get('page')
    paginator = Paginator(projects, objectPerPage)
    projects = paginator.get_page(page)
    
    return paginator, projects


def SearchProject(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tags)
    )
    return projects, search_query