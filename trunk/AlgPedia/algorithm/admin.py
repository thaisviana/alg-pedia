from django.contrib import admin
from algorithm.models import Author, ProgrammingLanguage, Classification, Algorithm, Implementation

class ClassificationAdmin(admin.ModelAdmin):
	list_display = ('name', 'uri')
	search_fields = ('name',)
	
class AlgorithmAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'classification')
	search_fields = ('name', 'classification__name')
	
class ImplementationAdmin(admin.ModelAdmin):
	list_display = ('algorithm', 'programming_language')
	search_fields = ('algorithm', 'programming_language')

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'uri')
	search_fields = ('name',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(ProgrammingLanguage)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Implementation, ImplementationAdmin)
