from django.contrib import admin
from algorithm.models import Author, ProgrammingLanguage, Classification, Algorithm, Implementation

class ClassificationAdmin(admin.ModelAdmin):
	list_display = ('name', 'uri')
	search_fields = ('name',)

admin.site.register(Author)
admin.site.register(ProgrammingLanguage)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Algorithm)
admin.site.register(Implementation)
