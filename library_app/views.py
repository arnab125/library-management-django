from django.shortcuts import render

from .models import Book


# Create your views here.


def landing(request):
    return render(request, 'landing.html')\


def view_books(request):
    books = Book.objects.all()
    print("hi")
    print(books)
    return render(request, 'viewbooks.html', context={'books': books})