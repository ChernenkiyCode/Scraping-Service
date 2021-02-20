from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    if request.user.is_authenticated:
        form = FindForm(initial={'name': request.user.city, 'language': request.user.language})
    else:
        form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('name')
    language = request.GET.get('language')
    _filter = {}
    if city:
        _filter['city__slug'] = city
    if language:
        _filter['language__slug'] = language

    qs = Vacancy.objects.filter(**_filter)
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'scraping/list.html', {'object_list': page_obj, 'form': form})
