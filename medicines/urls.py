from django.urls import path
from . import views

urlpatterns = [
    path('medicine/<int:id>', views.medicine_view, name='medicines'),
    path('search', views.search_results_view, name='search_results'),
    path('', views.search_page_view, name='search_page'),
]
