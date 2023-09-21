from django.urls import path
from books.views import create_section, edit_section, view_book

urlpatterns = [
    path('create-section/<int:book_id>', create_section, name = 'create_section'),
    path('view-section/<int:section_id>', edit_section, name = 'view_section'),
    path('book/<int:book_id>', view_book, name='view_book'),
]