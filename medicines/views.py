from django.shortcuts import render
from django.http import Http404

from .models import Medicine
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.
def medicine_view(req, id, *args, **kwargs):
    try:
        obj = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        raise Http404

    return render(req, 'medicine.djt', {'obj': obj})


def search_page_view(req, *args, **kwargs):
    return render(req, 'search.djt', {})


def search_results_view(req, *args, **kwargs):
    query = req.GET.get('q', '')

    results = Medicine.objects.annotate(
        similarity=TrigramSimilarity('name', query),
    ).filter(similarity__gt=0.3).order_by('-similarity')

    context = {
        'results': results,
        'query': query
    }

    return render(req, 'results.djt', context)
