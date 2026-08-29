from .models import Course


def navbar_courses(request):
    return {
        'navbar_courses': Course.objects.all().order_by('category', 'title')[:12]
    }
