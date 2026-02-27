from django.urls import path
from . import views

urlpatterns = [
    path('api/',               views.book_list_create, name='book-list-create'),
    path('api/search/',        views.book_search,      name='book-search'),
    path('api/<int:book_id>/', views.book_detail,      name='book-detail'),
]