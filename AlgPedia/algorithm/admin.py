from django.contrib import admin
from algorithm.models import Author, ProgrammingLanguage, Classification, Algorithm, Implementation

class ClassificationAdmin(admin.ModelAdmin):
	list_display = ('name', 'uri')
	search_fields = ('name',)
	
class AlgorithmAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'classification')
	search_fields = ('name', 'classification')

admin.site.register(Author)
admin.site.register(ProgrammingLanguage)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Implementation)
