from django.shortcuts import render
from django.http import Http404

from .models import Medicine


# Create your views here.
def medicine_view(req, id, *args, **kwargs):
    try:
        obj = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        raise Http404

    return render(req, 'medicines/index.html', {'obj': obj})
