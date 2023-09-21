from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from books.models import Book, BookUserRole, COLLABORATOR, Section
from users.models import CustomUser

#create section or subsections for a book
def create_section(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    try:
        user_role = BookUserRole.objects.get(user=request.user, book=book)

    except BookUserRole.DoesNotExist:
        return HttpResponseForbidden("You don't have a role in this book.")
    if not user_role.is_author():
        return HttpResponseForbidden("Only authors can create sections.")

    if request.method == "POST":
        section_title = request.POST.get('new_section_title')

        parent_section_id = request.POST.get('parent_section')
        parent_section = None
        if parent_section_id:
            parent_section = get_object_or_404(Section, id=parent_section_id)

        Section.objects.create(title=section_title, book=book, parent_section=parent_section)
        if parent_section:
            return redirect('view_section', section_id=parent_section.id)
        else:
            return redirect('view_book', book_id=book_id)

    return render(request, 'create_section.html', {'book': book})


# This is to view and edit the content of a section
def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    try:
        user_role = BookUserRole.objects.get(user=request.user, book=section.book)
    except BookUserRole.DoesNotExist:
        return HttpResponseForbidden("You don't have a role in this book.")

    if request.method == "POST":
        if 'add_subsection' in request.POST and user_role.is_author():
            subsection_title = request.POST.get('subsection_title')
            Section.objects.create(title=subsection_title, book=section.book, parent_section=section)
            return redirect('view_section', section_id=section.id)
        section_title = request.POST.get('section_title')
        section_content = request.POST.get('section_content')

        section.title = section_title
        section.content = section_content
        section.save()

        return redirect('view_section', section_id=section.id)  # Assuming a view to see the edited section.

    return render(request, 'view_section.html', {'section': section, 'user_role':user_role})


# Detail for the books such as author, collaborators, and sections
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_role = BookUserRole.objects.get(user=request.user, book=book)
    context = {'book':book, 'user_role':user_role}
    if user_role.is_author():
        if request.method == 'POST':
            if 'add_collaborator' in request.POST:
                collaborator_id = request.POST.get('collaborator')
                collaborator = CustomUser.objects.get(pk=collaborator_id)
                book.collaborators.add(collaborator)

            elif 'remove_collaborator' in request.POST:
                collaborator_id = request.POST.get('remove_collaborator_id')
                collaborator = CustomUser.objects.get(pk=collaborator_id)
                book.collaborators.remove(collaborator)
                BookUserRole.objects.filter(user=collaborator, book=book).delete()

            return redirect('view_book', book_id=book.id)

        context['users'] = CustomUser.objects.exclude(
            id__in=[request.user.id] + [collab.id for collab in book.collaborators.all()])

    return render(request, 'book_detail.html', context=context)

