from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    publication_date = models.DateField()
    number_of_copies_available = models.IntegerField()


    def __str__(self):
        return self.title