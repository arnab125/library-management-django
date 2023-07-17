from django.urls import path
from .views import landing, view_books, view_books_search, signup_view, login_view, logout_view, view_wishlist, add_to_wishlist, remove_from_wishlist




urlpatterns = [
    path('register/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('landing/', landing, name='landing'),
    path('view_books/', view_books, name='view_books'),
    path('view_books/search/<str:search_term>/', view_books_search, name='view_books_search'),
    path('add_to_wishlist/<str:isbn>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<str:isbn>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('view_wishlist/', view_wishlist, name='view_wishlist'),
]