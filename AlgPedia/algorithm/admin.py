from django.contrib import admin
from algorithm.models import Author, ProgrammingLanguage, Classification, Algorithm, Implementation

admin.site.register(Author)
admin.site.register(ProgrammingLanguage)
admin.site.register(Classification)
admin.site.register(Algorithm)
admin.site.register(Implementation)
