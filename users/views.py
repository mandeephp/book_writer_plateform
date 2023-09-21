from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from books.models import Book


# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_profile')  # Redirect to a user profile after login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    authored_books = request.user.authored_books.all()
    collaborated_books = request.user.collaborated_books.all()

    context = {
        'user': request.user,
        'authored_books': authored_books,
        'collaborated_books': collaborated_books
    }
    if request.method == "POST":
        title = request.POST.get('book_title')
        if Book.objects.filter(title=title).exists():
            context['error_message'] ='A book with this title already exists.'
            context['form_data'] =request.POST
            return render(request, 'user_profile.html', context)
        new_book = Book(title=title, author=request.user)
        new_book.save()
        return redirect('user_profile')
    return render(request, 'user_profile.html', context)