from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30)
    uri = models.URLField()

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=10)

class Classification(models.Model):
    name = models.CharField(max_length=35)

class Algorithm(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(Author, null=True, blank=True)
    classification = models.ForeignKey(Classification, null=True, blank=True)
    
class Implementation(models.Model):
    # an algorithm can have many implementations
    algorithm = models.ForeignKey(Algorithm)
    code = models.TextField()
    programming_language = models.OneToOneField(ProgrammingLanguage)