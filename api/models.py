from django.db import models

class Book(models.Model):
    title      = models.CharField(max_length=200)
    author     = models.CharField(max_length=100)
    year       = models.IntegerField()
    genre      = models.CharField(max_length=80, default='Unknown')
    isbn       = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def to_dict(self):
        return {
            'id':         str(self.id),
            'title':      self.title,
            'author':     self.author,
            'year':       str(self.year),
            'genre':      self.genre,
            'isbn':       self.isbn or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }