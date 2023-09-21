from django.db import models
from users.models import CustomUser

AUTHOR = '1'
COLLABORATOR = '2'

ROLE_CHOICES = (
        (AUTHOR, 'Author'),
        (COLLABORATOR, 'Collaborator'),
    )


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="authored_books")
    collaborators = models.ManyToManyField(CustomUser, related_name="collaborated_books", blank=True)

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)

        BookUserRole.objects.get_or_create(user=self.author, book=self, role=AUTHOR)

        for collaborator in self.collaborators.all():
            BookUserRole.objects.get_or_create(user=collaborator, book=self, role=COLLABORATOR)

    def main_sections(self):
        return self.sections.filter(parent_section__isnull=True)
    class Meta:
        db_table = 'books'
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"

class Section(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subsections')

    class Meta:
        unique_together = ['title', 'book']
        db_table = 'sections'
        verbose_name = "Section"
        verbose_name_plural = "Sections"

class BookUserRole(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    def is_author(self):
        return self.role == AUTHOR

    class Meta:
        db_table = 'book_user_roles'
        unique_together = ['user', 'book']
        verbose_name = "Book User Role"
        verbose_name_plural = "Book User Roles"