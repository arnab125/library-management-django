import datetime

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
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    borrowed_books_isbn_list = [book.book.isbn for book in borrowed_books]
    isbn_list = [book.book.isbn for book in wishlist]
    return render(request, 'viewbooks.html', context={'books': books, 'wishlist': isbn_list, 'borrowed_books': borrowed_books_isbn_list})

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
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    borrowed_books_isbn_list = [book.book.isbn for book in borrowed_books]
    print(borrowed_books_isbn_list)
    return render(request, 'wishlist.html', context={'wishlist': wishlist, 'length_wishlist': len(wishlist), 'borrowed_books': borrowed_books_isbn_list})


def borrow_book(request, isbn):
    user = request.user
    book = Book.objects.get(isbn=isbn)
    borrowed_date = datetime.date.today()
    due_date = borrowed_date + datetime.timedelta(days=7)
    borrowed_book = BorrowedBook.objects.create(user=user, book=book, borrowed_date=borrowed_date, due_date=due_date)
    book.number_of_copies_available -= 1
    book.save()
    return redirect('view_books')

def return_book(request, isbn):
    user = request.user
    book = Book.objects.get(isbn=isbn)
    borrowed_book = BorrowedBook.objects.filter(user=user, book=book)
    borrowed_book.delete()
    book.number_of_copies_available += 1
    book.save()
    return redirect('view_borrowed_books')

def view_borrowed_books(request):
    user = request.user
    borrowed_books = BorrowedBook.objects.filter(user=user)
    return render(request, 'borrowed_books.html', context={'borrowed_books': borrowed_books, 'length_borrowed_books': len(borrowed_books)})


def extra_fines(request):
    total_fine = 0
    number_of_books = 0
    user = request.user
    borrowed_books = BorrowedBook.objects.filter(user=user)
    book_details_list = []
    for book in borrowed_books:
        if datetime.date.today() > book.due_date:
            delay = (datetime.date.today() - book.due_date).days
            fine = delay * 5
            book_details = {'title': book.book.title, 'delay': delay, 'fine': fine}
            book_details_list.append(book_details)
            number_of_books += 1
            total_fine += fine
    return render(request, 'extra_fines.html', context={'total_fine': total_fine, 'number_of_books': number_of_books, 'details': book_details_list})

def get_notifications(request):
    user = request.user
    due_date_list = []
    borrowed_books = BorrowedBook.objects.filter(user=user)
    for book in borrowed_books:
        if book.due_date -datetime.date.today() <= datetime.timedelta(days=30):
            due_date_list.append({'title': book.book.title, 'due_date': book.due_date})
            print(due_date_list)
    return render(request, 'notifications.html', context={'due_date_list': due_date_list})