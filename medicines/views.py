from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404

from .models import Medicine
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.
def medicine_view(req, id, *args, **kwargs):
    try:
        obj = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        raise Http404

    page = req.GET.get('page', 1)

    info_all = obj.info_set.all()

    info = Paginator(info_all, 12).get_page(page)

    context = {
        'info': info,
        'obj': obj
    }

    return render(req, 'medicine.djt', context)


def search_page_view(req, *args, **kwargs):
    return render(req, 'search.djt', {})


def search_results_view(req, *args, **kwargs):
    query = req.GET.get('q', '')

    page = req.GET.get('page', 1)

    results = Medicine.objects.annotate(
        similarity=TrigramSimilarity('name', query),
    ).filter(similarity__gt=0.3).order_by('-similarity')

    results = Paginator(results, 10).get_page(page)

    context = {
        'results': results,
        'query': query
    }

    return render(req, 'results.djt', context)
