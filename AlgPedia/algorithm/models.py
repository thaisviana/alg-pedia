from django.db import models

class ProgrammingLanguage(models.Model):
	name = models.CharField(max_length=10)
	
	def __unicode__(self):
		return u'%s' % self.name

class Classification(models.Model):
	name = models.CharField(max_length=35)
	uri = models.URLField()
	
	def get_show_url(self):
		return "http://localhost:8000/show/cat/id/%i" % self.id 
	
	def __unicode__(self):
		return u'%s' % self.name
		
class Algorithm(models.Model):
	name = models.CharField(max_length=30)
	description = models.TextField()
	classification = models.ForeignKey(Classification, null=True, blank=True)
	uri = models.URLField()
	visible = models.BooleanField()
	
	def get_show_url(self):
		return "http://localhost:8000/show/alg/id/%i" % self.id
	
	def __unicode__(self):
		return u'%s' % self.name.lower().title()

class Implementation(models.Model):
	# an algorithm can have many implementations
	algorithm = models.ForeignKey(Algorithm)
	code = models.TextField()
	programming_language = models.ForeignKey(ProgrammingLanguage)
	visible = models.BooleanField()
	
	def __unicode__(self):
		return u'%s' % self.code
	
	def get_show_url(self):
		return "http://localhost:8000/show/imp/id/%i" % self.id