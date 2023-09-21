from django.contrib import admin

from books.models import Book, BookUserRole, Section

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author' )


class BookUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'role' )

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'book', 'parent_section' )

admin.site.register(Book, BookAdmin)
admin.site.register(BookUserRole, BookUserRoleAdmin)
admin.site.register(Section, SectionAdmin)