from django.shortcuts import render

from .models import Book, Wishlist, BorrowedBook


# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_books')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def landing(request):
    return render(request, 'landing.html')\


def view_books(request):
    books = Book.objects.all()
    wishlist = Wishlist.objects.filter(user=request.user)
    isbn_list = [book.book.isbn for book in wishlist]
    return render(request, 'viewbooks.html', context={'books': books, 'wishlist': isbn_list})

def view_books_search(request, search_term):
    if search_term:
        books = Book.objects.filter(title__icontains=search_term)
    else:
        books = Book.objects.all()
    return render(request, 'viewbooks.html', context={'books': books})


def add_to_wishlist(request, isbn):
    user = request.user
    book = Book.objects.get(isbn=isbn)
    wishlist = Wishlist.objects.create(user=user, book=book)
    return redirect('view_wishlist')

def remove_from_wishlist(request, isbn):
    user = request.user
    book = Book.objects.get(isbn=isbn)
    wishlist = Wishlist.objects.filter(user=user, book=book)
    wishlist.delete()
    return redirect('view_wishlist')

def view_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    for item in wishlist:
        print(item.book.title)
    return render(request, 'wishlist.html', context={'wishlist': wishlist, 'length_wishlist': len(wishlist)})
