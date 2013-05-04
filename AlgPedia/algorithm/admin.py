from django.contrib import admin
from algorithm.models import ProgrammingLanguage, Classification, Algorithm, Implementation

class ClassificationAdmin(admin.ModelAdmin):
	list_display = ('name', 'uri')
	search_fields = ('name',)
	
class AlgorithmAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'classification', 'visible')
	search_fields = ('name', 'classification__name', 'visible')
	
class ImplementationAdmin(admin.ModelAdmin):
	list_display = ('algorithm', 'programming_language', 'visible')
	search_fields = ('algorithm', 'programming_language', 'visible')

admin.site.register(ProgrammingLanguage)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Implementation, ImplementationAdmin)
