from django.urls import path
from .views import landing, view_books


app_name = 'transactions'


urlpatterns = [
    path('landing/', landing, name='landing'),
    path('view_books/', view_books, name='view_books'),
]